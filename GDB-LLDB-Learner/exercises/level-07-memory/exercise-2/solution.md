# 解决方案

```
(gdb) print ptr
$1 = (int *) 0x7fffffffddf4
(gdb) print *ptr
$2 = 42
(gdb) print ptr_ptr
$3 = (int **) 0x7fffffffddf8
(gdb) print *ptr_ptr
$4 = (int *) 0x7fffffffddf4
(gdb) print **ptr_ptr
$5 = 42
(gdb) x/4xw ptr
```
