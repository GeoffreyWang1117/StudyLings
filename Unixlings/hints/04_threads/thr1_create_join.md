## 提示 1
`pthread_create` 的第 4 个参数只是一个指针，新线程"稍后某个时刻"才去读它指向的内容。
`&i` 指向的是 main 栈上唯一的那个循环变量，main 继续循环时它会被改写 —— 线程读到的是谁的 i 全凭运气。

## 提示 2
参数的生命周期必须覆盖到线程读完为止。最简单的办法：`tasks` 数组（已经 calloc 好了）里每个线程一个元素，
先填好 `tasks[i].lo/hi`，再 `pthread_create(&tids[i], nullptr, worker, &tasks[i])`；
worker 里 `struct task *t = arg;`，不再需要全局的 `g_tasks` 和下标。

## 提示 3
结果也放进这个结构体（`t->partial`）。`pthread_join` 建立了 happens-before 关系：
join 返回之后 main 读 `tasks[i].partial` 是安全的，不需要锁。
（也可以用 `pthread_exit`/返回值传结果，但返回指针就要考虑谁来 free。）
