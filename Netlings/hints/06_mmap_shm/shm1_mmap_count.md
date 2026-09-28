## 提示 1
流程：`open` → `fstat` 取 `st_size` → `mmap` → 扫描 → `munmap` → `close`。
mmap 失败返回的是 `MAP_FAILED`（即 `(void *)-1`），不是 `nullptr`。

## 提示 2
空文件：`if (size > 0) { ... mmap ... }`。另一个隐藏的坑：映射之后文件被别人截短，
访问超出文件末尾的整页会收到 SIGBUS —— 生产代码（如 LMDB）要么加锁，要么捕获 SIGBUS。

## 提示 3
数行：`while ((nl = memchr(p, '\n', end - p)) != nullptr) { lines++; p = nl + 1; }`。
对比一下：`strace -e trace=read,mmap ./shm1_mmap_count big.txt` —— 文件内容一次 read 都没有，
数据是缺页异常时由内核从 page cache 直接映射进来的。
