#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

/*
 * 多线程示例程序
 * 演示如何调试多线程程序
 */

int shared_counter = 0;

void* worker_thread(void* arg) {
    int thread_id = *(int*)arg;

    for (int i = 0; i < 5; i++) {
        printf("线程 %d: 迭代 %d\n", thread_id, i);
        shared_counter++;  // 竞态条件！
        sleep(1);
    }

    printf("线程 %d 完成\n", thread_id);
    return NULL;
}

int main() {
    pthread_t thread1, thread2;
    int id1 = 1, id2 = 2;

    printf("创建线程...\n");

    pthread_create(&thread1, NULL, worker_thread, &id1);
    pthread_create(&thread2, NULL, worker_thread, &id2);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("最终计数器值: %d (期望: 10)\n", shared_counter);

    return 0;
}
