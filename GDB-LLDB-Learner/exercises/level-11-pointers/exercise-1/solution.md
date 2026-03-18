# Exercise 1: 完整解决方案

## 内存布局示例

假设在我的系统上：
```
value 地址: 0x7fffffffddf0, 值: 42
p1    地址: 0x7fffffffddf8, 值: 0x7fffffffddf0, *p1: 42
p2    地址: 0x7fffffffe000, 值: 0x7fffffffddf8, *p2: 0x7fffffffddf0, **p2: 42
p3    地址: 0x7fffffffe008, 值: 0x7fffffffe000, *p3: 0x7fffffffddf8, **p3: 0x7fffffffddf0, ***p3: 42
```

图示:
```
0xddf0: [42]        ← value
         ↑
0xddf8: [0xddf0]    ← p1
         ↑
0xe000: [0xddf8]    ← p2
         ↑
0xe008: [0xe000]    ← p3
```

## GDB 完整会话

```
(gdb) print sizeof(int*)
$1 = 8  # 64位系统

(gdb) x/4gx &value
0x7fffffffddf0: 0x000000000000002a  0x00007fffffffddf0
0x7fffffffe000: 0x00007fffffffddf8  0x00007fffffffe000
```

每行显示:
- 第1行: value 的值(0x2a=42), p1 的值(value的地址)
- 第2行: p2 的值(p1的地址), p3 的值(p2的地址)
