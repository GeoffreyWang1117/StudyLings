// EXERCISE: proc6_exit_vs__exit — 子进程调用 exit() 删掉了父进程的 pidfile
// TOPIC: exit vs _exit / atexit / fork 后子进程的收尾
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §7.3 进程终止（atexit，图 7.2）、§8.3 fork、§8.5 exit；man 3 exit、man 2 _exit
// I AM NOT DONE
//
// 说明：
//   用法：proc6_exit_vs__exit PIDFILE
//   一个"守护进程"的典型骨架：
//   - 启动时写 PIDFILE（内容是自己的 pid），并用 atexit 注册 cleanup：删除 PIDFILE、打印 "cleanup"
//   - 打印 "starting <pid>"，然后 fork 一个子进程干活：子进程打印 "child working"
//   - 父进程回收子进程，检查 PIDFILE 是否还在：在则打印 "pidfile ok"，否则 "pidfile GONE"
//   - 父进程 return 0 → exit → cleanup 运行一次
//
//   exit(3) 是 C 库函数：先按注册的逆序运行 atexit 处理函数，再 flush 并关闭所有 FILE*，
//   最后调用 _exit(2)。_exit 直接进内核结束进程，什么收尾都不做。
//   子进程是父进程的"复制品"，继承了 atexit 列表和 stdio 缓冲区，但这些资源属于父进程 ——
//   如果子进程调用 exit()，就会替父进程删 pidfile、重复输出缓冲区里的内容。
//
//   测试会把 stdout 接到管道，检查："cleanup" 恰好 1 次、"starting" 恰好 1 次、
//   "child working" 恰好 1 次、父进程看到 "pidfile ok"、程序结束后 PIDFILE 已被删除。
//
//   为什么重要：Python multiprocessing / subprocess 在 fork 出的子进程里只用 os._exit；
//   Redis 的 BGSAVE 子进程结束时调用 exitFromChild() → _exit；
//   C++ 程序里子进程 exit() 还会运行全局对象的析构函数，可能关掉父进程的数据库连接、日志文件。

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static const char *g_pidfile;

static void cleanup(void) {
    if (unlink(g_pidfile) < 0)
        perror("unlink pidfile");
    printf("cleanup\n");
}

static void child_work(void) {
    printf("child working\n");
}

int main(int argc, char *argv[]) {
    // 注意：这里故意**不**调用 setvbuf —— stdout 接管道时是全缓冲
    if (argc != 2) {
        fprintf(stderr, "usage: %s PIDFILE\n", argv[0]);
        return 2;
    }
    g_pidfile = argv[1];

    FILE *f = fopen(g_pidfile, "wx");
    if (!f) {
        perror(g_pidfile);
        return 1;
    }
    fprintf(f, "%d\n", (int)getpid());
    if (fclose(f) == EOF) {
        perror("fclose");
        return 1;
    }
    if (atexit(cleanup) != 0) {
        fprintf(stderr, "atexit failed\n");
        return 1;
    }

    printf("starting %d\n", (int)getpid());

    // TODO: fork 前需要做什么，才能保证 "starting" 不会被子进程重复输出？

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    if (pid == 0) {
        child_work();
        // TODO: 子进程结束。不能运行父进程注册的 atexit 处理函数，但自己的输出不能丢
        exit(0); // BUG: 子进程运行了父进程的 cleanup（删 pidfile），还重复 flush 了继承来的缓冲区
    }

    int status;
    while (waitpid(pid, &status, 0) < 0) {
        if (errno != EINTR) {
            perror("waitpid");
            exit(1);
        }
    }
    printf("pidfile %s\n", access(g_pidfile, F_OK) == 0 ? "ok" : "GONE");
    return 0; // 从 main 返回 == exit(0) → cleanup 在这里运行
}
