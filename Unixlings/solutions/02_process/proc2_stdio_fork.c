// EXERCISE: proc2_stdio_fork — fork 复制了 stdio 缓冲区："before fork" 为什么打印了两次？
// TOPIC: fork 与 stdio 缓冲 / fflush / _exit
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §8.3（图 8.1 的输出重定向到文件时的现象）、§5.4 缓冲、§5.5 setvbuf
//
// 说明：
//   用法：proc2_stdio_fork NCHILD      （1 <= NCHILD <= 10，默认 2）
//   程序先 printf("before fork\n")，再 fork NCHILD 个子进程，每个子进程打印一行
//   "child <i> pid <pid>"，父进程回收它们后打印 "parent reaped <NCHILD>"。
//
//   在终端里运行一切正常；但把 stdout 接到管道或文件（./proc2_stdio_fork | cat），
//   "before fork" 就会出现 NCHILD+1 次！原因：stdout 指向终端时是行缓冲，指向管道/文件时是
//   全缓冲 —— "before fork\n" 还躺在用户态缓冲区里没 write，fork 把整个地址空间（包括这个
//   缓冲区）复制给了子进程，于是每个进程退出时都 flush 一遍。
//
//   修复要点：
//   1. fork 前 fflush(stdout)（以及 stderr 之外所有你写过的 FILE*）
//   2. 子进程结束时用 _exit 而不是 exit —— exit 会再 flush 一遍从父进程继承来的缓冲区、
//      再跑一遍 atexit 处理函数；子进程自己打印的内容要在 _exit 前自己 fflush
//   测试会把 stdout 接到管道和文件，检查每一行都恰好出现一次。
//
//   为什么重要：日志重复是 prefork 服务器（Apache prefork、gunicorn、PHP-FPM）和
//   Python multiprocessing 的经典坑；Python 的 os.fork() 文档专门提醒先 sys.stdout.flush()，
//   subprocess 在 fork 后的子进程里只用 os._exit。

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    // 注意：这里故意**不**调用 setvbuf —— stdout 接管道时保持默认的全缓冲，这正是本题的现场
    int nchild = argc > 1 ? atoi(argv[1]) : 2;
    if (nchild < 1 || nchild > 10) {
        fprintf(stderr, "usage: %s [NCHILD 1..10]\n", argv[0]);
        return 2;
    }

    printf("before fork\n");

    // TODO: fork 之前把 stdout 缓冲区里的内容真正写出去
    if (fflush(stdout) == EOF) {
        perror("fflush");
        return 1;
    }

    for (int i = 1; i <= nchild; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            return 1;
        }
        if (pid == 0) {
            printf("child %d pid %d\n", i, (int)getpid());
            // TODO: 子进程该怎样结束？自己的输出要先 flush，然后用不会再次 flush 继承缓冲区的方式退出
            fflush(stdout);
            _exit(0);
        }
    }

    for (int reaped = 0; reaped < nchild;) {
        if (waitpid(-1, nullptr, 0) < 0) {
            if (errno == EINTR)
                continue;
            perror("waitpid");
            return 1;
        }
        reaped++;
    }
    printf("parent reaped %d\n", nchild);
    return 0;
}
