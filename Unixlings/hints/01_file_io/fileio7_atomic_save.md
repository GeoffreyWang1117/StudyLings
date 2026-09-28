## 提示 1
临时文件名模板：`snprintf(tmp, sizeof tmp, "%s.tmpXXXXXX", path); int fd = mkostemp(tmp, O_CLOEXEC);`
mkstemp 创建的文件权限是 0600，需要的话 `fchmod(fd, 0644)`。

## 提示 2
顺序：写完 → `fsync(fd)` → `close(fd)` → `rename(tmp, path)` → 打开 `dirname(path)` 目录 → `fsync(dirfd)`。
中途任一步失败：保存 errno，`unlink(tmp)`，恢复 errno，返回 -1。

## 提示 3
dirname() 可能修改传入的字符串，先拷贝一份。
Linux 还有更现代的写法：`open(dir, O_TMPFILE | O_WRONLY)` 创建匿名文件，写完后 `linkat` 到临时名再 rename。
