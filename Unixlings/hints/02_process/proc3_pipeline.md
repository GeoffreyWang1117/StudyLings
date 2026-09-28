## 提示 1
管道的读端只有在**所有**写端都被关闭后才会读到 EOF。fork 之后，父进程和两个子进程各有一份
`fds[0]`、`fds[1]`。数一数：`wc` 等 EOF 时，还有谁拿着写端？父进程 fork 完就该 `close(fds[0]); close(fds[1]);`。

## 提示 2
子进程里 `dup2(fds[1], STDOUT_FILENO)` 之后，原始的 `fds[1]` 已经没用了，但 exec 会把它原样带进新程序。
与其在每个子进程里手动 close，不如用 `pipe2(fds, O_CLOEXEC)` 创建：exec 时内核自动关闭它们，
而 dup2 出来的新 fd 不继承 CLOEXEC 标志，会保留下来。

## 提示 3
退出码：`WIFEXITED(st) ? WEXITSTATUS(st) : 128 + WTERMSIG(st)`，只看 cmd2 的 status（`sh` 默认就是这样，
`bash` 的 `set -o pipefail` 才会看其他阶段）。两个子进程都要 waitpid，否则会留下僵尸。
