## 提示 1
`fstatat(dirfd, e->d_name, &st, AT_SYMLINK_NOFOLLOW)` 等价于"相对于 dirfd 的 lstat"。

## 提示 2
递归：`int sub = openat(dirfd, e->d_name, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC); walk(sub, path);`
O_NOFOLLOW 是第二道保险：就算在 fstatat 和 openat 之间目录被换成了符号链接，openat 也会失败（ELOOP）。

## 提示 3
fdopendir 接管 fd 的所有权：成功以后不要再 close(fd)，closedir 会关它；失败时才需要自己 close。
