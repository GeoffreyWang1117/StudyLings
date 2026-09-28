## 提示 1
顺序：`fflush(stdout)` → `saved = dup(1)` → `open` → `dup2(fd, 1)` → `close(fd)` → `return saved`。

## 提示 2
恢复同样要先 `fflush(stdout)`，然后 `dup2(saved, 1)`、`close(saved)`。

## 提示 3
想亲眼看到缓冲问题：把程序输出接到 `| cat` 和直接输出到终端对比 —— 终端是行缓冲，管道是全缓冲。
`setvbuf(stdout, NULL, _IONBF, 0)` 可以关掉缓冲，但正确做法是在切换 fd 之前 fflush。
