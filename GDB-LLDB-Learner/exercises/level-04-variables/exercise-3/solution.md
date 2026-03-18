# Exercise 3: 解决方案

```bash
(gdb) break main
(gdb) run
(gdb) print numbers
$1 = {10, 20, 30, 40, 50}
(gdb) print numbers[0]@5
$2 = {10, 20, 30, 40, 50}
(gdb) print *numbers@5
$3 = {10, 20, 30, 40, 50}
(gdb) print matrix
$4 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
(gdb) print matrix[1]
$5 = {4, 5, 6}
```

LLDB:
```
(lldb) parray 5 numbers
(lldb) p numbers
(int [5]) $0 = ([0] = 10, [1] = 20, ...)
```
