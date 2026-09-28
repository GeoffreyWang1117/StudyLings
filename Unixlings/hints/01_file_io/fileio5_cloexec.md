## 提示 1
`open(path, O_RDONLY | O_CLOEXEC)`，`eventfd(0, EFD_CLOEXEC)`。

## 提示 2
自己看看泄漏：`./build/dev/bin/fileio5_cloexec /etc/passwd ls -l /proc/self/fd`。
修复前能在列表里看到 /etc/passwd 和 anon_inode:[eventfd]。

## 提示 3
接手一个老代码库、没法逐个改创建点时：在 exec 之前调用 `close_range(3, ~0U, CLOSE_RANGE_CLOEXEC)`
把 3 以上的所有 fd 一次性标记为 CLOEXEC（systemd、新版 Python subprocess 就是这么做的）。
