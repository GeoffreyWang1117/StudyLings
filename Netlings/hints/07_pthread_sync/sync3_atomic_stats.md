## 提示 1
`static atomic_ulong g_requests;` 然后 `atomic_fetch_add_explicit(&g_requests, 1, memory_order_relaxed);`。
relaxed 足够：计数器之间没有先后要求，join 之后主线程读到的一定是最终值（pthread_join 本身就是同步点）。

## 提示 2
指针发布是另一回事：worker 拿到指针后要读 `cfg->bucket_width_us`，这个字段是主线程在发布**之前**写的。
只有"release 写 + acquire 读到同一个值"才建立 happens-before，把之前的写"带"过去。

## 提示 3
x86 上 relaxed 和 acquire/release 的 load/store 生成的指令几乎一样（都是普通 mov），所以"在我机器上没问题"；
区别在于编译器重排和弱内存序 CPU（ARM、POWER、RISC-V）。TSan 按 C11 模型检查，不看你用的是什么 CPU。
