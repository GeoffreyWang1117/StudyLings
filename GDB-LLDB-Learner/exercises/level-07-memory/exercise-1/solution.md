# 解决方案

```
(gdb) break main
(gdb) run
(gdb) next  # 跳过初始化
(gdb) x/20xb &buffer
0x7fffffffddf0: 0x48 0x65 0x6c 0x6c 0x6f 0x00 ...
(gdb) x/5d numbers
0x7fffffffde00: 1 2 3 4 5
(gdb) x/s ptr
0x555555556004: "World"
```

格式: x/Nfu addr
- N: 数量
- f: 格式 (x=hex, d=dec, s=string, i=instruction)
- u: 单位 (b=byte, h=half, w=word, g=giant)
