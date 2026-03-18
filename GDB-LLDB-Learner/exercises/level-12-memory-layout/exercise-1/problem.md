# Exercise 1: 结构体对齐和Padding

## 学习目标

- 理解结构体内存对齐规则
- 掌握 padding 的产生原因
- 学习如何优化结构体布局
- 理解 `__attribute__((packed))` 的作用
- 使用 `ptype /o` 查看详细布局

## 背景知识

### 对齐规则

1. **自然对齐**: 每个成员对齐到其类型大小的倍数
   - `char`: 1字节对齐
   - `short`: 2字节对齐
   - `int`: 4字节对齐
   - `double`: 8字节对齐

2. **结构体对齐**: 结构体大小是最大成员对齐数的倍数

3. **Padding**: 编译器插入的填充字节，确保对齐

### 为什么需要对齐？

- **性能**: CPU 访问对齐的数据更快
- **硬件要求**: 某些架构要求特定对齐
- **原子操作**: 对齐的数据可以原子访问

### 对齐示例

```c
struct Example {
    char a;      // 偏移 0, 大小 1
    // 3 字节 padding
    int b;       // 偏移 4, 大小 4
    char c;      // 偏移 8, 大小 1
    // 3 字节 padding (结构体对齐)
};
// 总大小: 12 字节
```

### 优化方法

**未优化** (24字节):
```c
struct Unoptimized {
    char a;      // 1 byte + 3 padding
    int b;       // 4 bytes
    char c;      // 1 byte + 7 padding
    double d;    // 8 bytes
};  // 总计: 24 字节
```

**优化** (16字节):
```c
struct Optimized {
    double d;    // 8 bytes
    int b;       // 4 bytes
    char a;      // 1 byte
    char c;      // 1 byte
    // 2 字节 padding
};  // 总计: 16 字节
```

## 任务

### 任务 1: 分析未优化结构体

**目标**: 理解 padding 如何产生

**步骤**:
1. 编译并运行程序
2. 在 GDB 中使用 `ptype /o struct Unoptimized`
3. 查看每个成员的偏移量
4. 计算 padding 的位置和大小

**问题**:
- `sizeof(struct Unoptimized)` 是多少？
- 成员 `a`, `b`, `c`, `d` 的偏移量分别是多少？
- 每个成员之后有多少 padding？
- 为什么 `b` 不能紧跟在 `a` 之后？

### 任务 2: 验证优化效果

**目标**: 理解成员顺序对内存的影响

**步骤**:
1. 使用 `ptype /o struct Optimized`
2. 比较优化前后的大小
3. 查看内存布局

**问题**:
- `sizeof(struct Optimized)` 是多少？
- 相比未优化版本，节省了多少字节？
- 优化的原理是什么？
- 是否还有 padding？在哪里？

### 任务 3: 理解 Packed 结构体

**目标**: 掌握禁用对齐的后果

**步骤**:
1. 查看 `struct Packed` 的布局
2. 比较 packed 和普通结构体的差异
3. 查看实际内存

**问题**:
- `sizeof(struct Packed)` 是多少？
- 是否有 padding？
- Packed 结构体的优缺点是什么？
- 什么时候应该使用 packed？

### 任务 4: 查看内存布局

**目标**: 可视化 padding 在内存中的表现

**步骤**:
1. 创建结构体实例 `u`, `o`, `p`
2. 使用 `x/24xb &u` 查看原始内存
3. 识别数据和 padding 的位置

**问题**:
- padding 字节的值是什么？
- 如何在内存中识别 padding？
- 不同成员的内存分布是怎样的？

## 编译和运行

```bash
make
./alignment

# GDB
gdb ./alignment

# LLDB
lldb ./alignment
```

## 预期输出

```
=== 结构体内存布局分析 ===

未优化结构体:
  sizeof(Unoptimized) = 24
  offsetof(a) = 0
  offsetof(b) = 4
  offsetof(c) = 8
  offsetof(d) = 16

优化结构体:
  sizeof(Optimized) = 16
  offsetof(d) = 0
  offsetof(b) = 8
  offsetof(a) = 12
  offsetof(c) = 13

Packed 结构体:
  sizeof(Packed) = 14

任务: 使用 GDB 查看实际内存布局
1. ptype /o struct Unoptimized
2. x/24xb &u  (查看内存，观察 padding)
3. 比较三种结构体的内存使用
```

## 调试提示

### 查看结构体布局 (GDB 7.8+)

```bash
(gdb) ptype /o struct Unoptimized
type = struct Unoptimized {
/*    0      |     1 */    char a;
/*    1      |     3 */    /* XXX 3-byte hole */
/*    4      |     4 */    int b;
/*    8      |     1 */    char c;
/*    9      |     7 */    /* XXX 7-byte hole */
/*   16      |     8 */    double d;
                           /* total size (bytes):   24 */
                         }
```

### 查看内存

```bash
# GDB
(gdb) p u
(gdb) x/24xb &u
(gdb) x/3xg &u    # 查看为 8 字节单位

# LLDB
(lldb) frame variable u
(lldb) memory read --size 1 --count 24 --format x `&u`
```

### 计算对齐

```bash
# GDB
(gdb) p offsetof(struct Unoptimized, b)
(gdb) p sizeof(struct Unoptimized)

# LLDB
(lldb) expr offsetof(Unoptimized, b)
```

## 常见对齐模式

### 1. 小结构体 (浪费)

```c
struct Small {
    char a;      // 1 + 3 padding
    int b;       // 4
};  // 总计: 8 字节 (37.5% 浪费)
```

### 2. 优化后 (紧凑)

```c
struct Compact {
    int b;       // 4
    char a;      // 1
    // 3 padding
};  // 总计: 8 字节 (仍有37.5%浪费，但无法更优)
```

### 3. 多字符 (填充空隙)

```c
struct Better {
    int b;       // 4
    char a1;     // 1
    char a2;     // 1
    char a3;     // 1
    char a4;     // 1
};  // 总计: 8 字节 (0% 浪费!)
```

## 跨平台差异

### 32位 vs 64位

| 类型 | 32位 | 64位 |
|------|------|------|
| char | 1 | 1 |
| short | 2 | 2 |
| int | 4 | 4 |
| long | 4 | 8 |
| pointer | 4 | 8 |
| double | 8 | 8 |

**影响**:
- 包含指针的结构体在64位系统上更大
- long 类型的结构体可能不兼容

### 编译器差异

- **GCC**: 默认自然对齐
- **MSVC**: 可通过 `#pragma pack` 控制
- **嵌入式**: 可能有特殊对齐要求

## 性能考虑

### 对齐访问 vs 非对齐访问

**对齐** (快):
```c
struct Aligned {
    int a;  // 偏移 0 (4的倍数)
    int b;  // 偏移 4 (4的倍数)
};  // CPU 可以一次访问
```

**非对齐** (慢):
```c
struct __attribute__((packed)) Unaligned {
    char x;
    int a;  // 偏移 1 (不是4的倍数!)
};  // CPU 可能需要两次访问
```

**性能影响**:
- x86: 2-3倍慢
- ARM: 可能崩溃（某些版本不支持非对齐访问）
- RISC-V: 硬件异常

### 缓存行对齐

```c
struct alignas(64) CacheLine {
    int data[16];  // 正好 64 字节
};  // 避免 false sharing
```

## 实际应用

### 1. 网络协议

```c
struct __attribute__((packed)) IPHeader {
    uint8_t version : 4;
    uint8_t ihl : 4;
    uint8_t tos;
    uint16_t total_length;
    // ... 必须精确匹配协议
};
```

### 2. 文件格式

```c
struct __attribute__((packed)) BMPHeader {
    uint16_t type;
    uint32_t size;
    // ... 必须与文件格式一致
};
```

### 3. 嵌入式寄存器

```c
struct __attribute__((packed)) Register {
    uint32_t enable : 1;
    uint32_t mode : 3;
    uint32_t reserved : 28;
};
```

## 扩展练习

### 1. 手动计算布局

为以下结构体计算每个成员的偏移量和总大小：

```c
struct Mystery {
    char a;
    short b;
    int c;
    char d;
    double e;
};
```

### 2. 优化真实结构体

```c
// 优化前
struct Config {
    bool enabled;      // 1
    int timeout;       // 4
    bool debug;        // 1
    double threshold;  // 8
    char name[10];     // 10
};

// 你的优化版本？
```

### 3. 跨平台兼容

编写一个结构体，在32位和64位系统上大小相同。

## 调试检查清单

- [ ] 使用 `ptype /o` 查看所有成员的偏移量
- [ ] 计算每个 padding 的大小
- [ ] 验证 `sizeof` 的值
- [ ] 查看实际内存，识别 padding
- [ ] 比较优化前后的差异
- [ ] 理解 packed 的影响

## 关键要点

1. **对齐是为了性能**: CPU 访问对齐数据更快
2. **Padding 自动插入**: 编译器保证对齐
3. **顺序很重要**: 重排序可以减少内存浪费
4. **Packed 有代价**: 节省空间但牺牲性能
5. **跨平台注意**: 不同架构对齐规则可能不同

## 总结

完成本练习后，你应该掌握：

1. ✅ 结构体对齐的基本规则
2. ✅ Padding 的产生和计算
3. ✅ 如何优化结构体布局
4. ✅ `__attribute__((packed))` 的用途
5. ✅ 使用调试器查看内存布局
6. ✅ 对齐对性能的影响

理解内存对齐是编写高效、可移植代码的关键！
