# Exercise 3: 解决方案

```bash
./assert_fail
10 / 2 = 5
assert_fail: assert_fail.c:5: divide: Assertion `b != 0 && "除数不能为零"' failed.
Aborted (core dumped)

gdb ./assert_fail core
(gdb) bt
#0  __pthread_kill_implementation
#1  __pthread_kill_internal
#2  raise
#3  abort
#4  __assert_fail
#5  divide (a=10, b=0) at assert_fail.c:5
#6  main () at assert_fail.c:13

(gdb) frame 5
#5  divide (a=10, b=0) at assert_fail.c:5
(gdb) print b
$1 = 0

(gdb) frame 6
#6  main () at assert_fail.c:13
13	    int result2 = divide(10, 0);
```

## 理解 Assertion
- Assertion 帮助及早发现错误
- 在 debug 版本启用，release 版本可禁用
- Core dump 包含完整的调用栈
- 可以看到 assertion 失败时的所有变量值

## 最佳实践
1. 使用有意义的 assertion 消息
2. 不要在 assertion 中放有副作用的代码
3. 在生产环境考虑是否启用 assertions
