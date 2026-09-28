## 提示 1
```c
static pthread_once_t g_crc_once = PTHREAD_ONCE_INIT;
pthread_once(&g_crc_once, build_crc_table);
```
pthread_once 保证 build_crc_table 只执行一次；其他同时调用的线程会**等它执行完**再返回，
所以返回后读表一定安全。别忘了检查它的返回值（pthread 函数出错时返回错误码，不设置 errno）。

## 提示 2
"双重检查锁定"（先无锁地看 initialized，再加锁再看一次）手写很容易错：
没有正确的内存序时，别的线程可能先看到 `initialized = true`，后看到表的内容。
把这种事交给 pthread_once / C11 call_once。

## 提示 3
`static thread_local int g_request_id;` —— 每个线程都有一份独立的变量，初始值为 0，线程退出时自动消失。
它是 APUE §12.6 里 `pthread_key_create` + `pthread_setspecific/getspecific` 的语言级版本
（需要析构函数、或动态创建 key 时才用 pthread_key）。
