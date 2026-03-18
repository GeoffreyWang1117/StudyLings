# Level 12: 内存布局和对齐专题

## 学习目标

- 理解结构体内存对齐规则
- 掌握 padding 和 packing 的概念
- 学习如何查看和优化内存布局
- 理解 union、bit fields 的内存表示
- 掌握不同平台的对齐差异

## 为什么学习内存布局？

- **性能优化**: 对齐的数据访问更快
- **内存效率**: 减少内存浪费
- **跨平台**: 理解不同平台的差异
- **调试**: 快速定位内存问题

## 对齐规则

### 基本规则

1. 结构体成员按声明顺序布局
2. 每个成员对齐到其自然边界
3. 结构体总大小是最大成员对齐数的倍数

### 对齐示例

```c
struct Example {
    char a;    // 1 字节，对齐到 1
    // 3 字节 padding
    int b;     // 4 字节，对齐到 4
    char c;    // 1 字节
    // 3 字节 padding (结构体对齐)
};
// 总大小: 12 字节
```

## GDB/LLDB 调试技巧

### 查看结构体布局

**GDB:**
```bash
(gdb) ptype /o struct Example
type = struct Example {
/*    0      |     1 */    char a;
/*    1      |     3 */    /* XXX 3-byte hole */
/*    4      |     4 */    int b;
/*    8      |     1 */    char c;
/*    9      |     3 */    /* XXX 3-byte padding */
                           /* total size (bytes):   12 */
                         }
```

**LLDB:**
```bash
(lldb) type lookup struct Example
```

### 查看实际内存

```bash
(gdb) x/12xb &my_struct
0x7fffffffe010: 0x41 0x00 0x00 0x00  0x2a 0x00 0x00 0x00
0x7fffffffe018: 0x42 0x00 0x00 0x00
```
