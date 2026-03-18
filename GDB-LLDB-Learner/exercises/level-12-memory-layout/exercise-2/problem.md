# Exercise 2: Union 和位域

## 学习目标

- 理解 union 的内存共享机制
- 掌握大小端序的观察方法
- 学习位域（bit fields）的使用
- 理解位域的内存压缩
- 探索网络协议头的位域应用

## 背景知识

### Union 内存共享

```c
union Data {
    int i;      // 4 字节
    float f;    // 4 字节
    char c[4];  // 4 字节
};
// sizeof(Data) = 4 (所有成员共享同一块内存)
```

**关键特性**:
- 所有成员共享同一块内存
- 大小等于最大成员的大小
- 修改一个成员会影响其他成员
- 同一时刻只能使用一个成员

### 位域（Bit Fields）

```c
struct Flags {
    unsigned int flag1 : 1;   // 1 位
    unsigned int flag2 : 1;   // 1 位
    unsigned int value : 6;   // 6 位
    unsigned int reserved : 24; // 24 位
};
// 总共 32 位 = 4 字节
```

**关键特性**:
- 压缩多个小值到一个字节/字
- 节省内存空间
- 适用于标志位、网络协议
- 顺序和填充由编译器决定

### 大小端序

**小端序** (Little Endian，x86):
```
数字 0x12345678 存储为:
地址: 0x00  0x01  0x02  0x03
值:   0x78  0x56  0x34  0x12
```

**大端序** (Big Endian，网络字节序):
```
数字 0x12345678 存储为:
地址: 0x00  0x01  0x02  0x03
值:   0x12  0x34  0x56  0x78
```

## 任务

### 任务 1: 探索 Union 的内存共享

**目标**: 理解 union 如何重用内存

**步骤**:
1. 创建 `union Data` 实例
2. 设置 `data.i = 0x41424344`
3. 查看 `data.c[]` 的值
4. 设置 `data.f = 3.14f`
5. 再次查看 `data.i` 和 `data.c[]`

**问题**:
- `sizeof(union Data)` 是多少？
- 设置 `data.i` 后，`data.c[]` 的值是什么？
- 这说明了什么字节序？
- 设置 `data.f` 后，原来的 `i` 值还在吗？

### 任务 2: 观察大小端序

**目标**: 使用 union 检测字节序

**步骤**:
1. 设置 `data.i = 0x01020304`
2. 查看 `data.c[0]`, `data.c[1]`, `data.c[2]`, `data.c[3]`
3. 判断系统是大端还是小端

**问题**:
- `data.c[0]` 的值是 0x01 还是 0x04？
- 如何通过 union 写一个字节序检测函数？
- 网络字节序是大端还是小端？

### 任务 3: 调试位域

**目标**: 理解位域的内存布局

**步骤**:
1. 创建 `struct Flags` 实例：`{flag1=1, flag2=0, value=42, reserved=0}`
2. 查看结构体的内存（4字节）
3. 计算每个位域的位置

**问题**:
- `sizeof(struct Flags)` 是多少？
- 4字节的内存中，各位域如何排列？
- 修改 `value` 从 42 到 63，内存如何变化？
- 位域能否跨字节边界？

### 任务 4: 网络协议头

**目标**: 理解位域在实际中的应用

**步骤**:
1. 检查 `struct PacketHeader` 的大小
2. 设置 `version=4`, `header_length=5`, `type_of_service=0`, `total_length=1500`
3. 查看原始内存

**问题**:
- 为什么 `version` 和 `header_length` 各占4位？
- 如何在一个字节中存储两个4位值？
- 这个结构体能否直接发送到网络？

## 编译和运行

```bash
make
./union_bits

# GDB
gdb ./union_bits

# LLDB
lldb ./union_bits
```

## 预期输出

```
=== Union 内存共享 ===
作为 int: 0x41424344
作为 bytes: DCBA
作为 float: 3.14
作为 bytes (hex): c3 f5 48 40

=== 位域 ===
sizeof(Flags) = 4
flag1=1, flag2=0, value=42

任务: 使用调试器查看 union 和位域的实际内存
```

## 调试提示

### 查看 Union

```bash
# GDB
(gdb) p data
(gdb) p data.i
(gdb) p data.f
(gdb) p data.c
(gdb) x/4xb &data

# LLDB
(lldb) frame variable data
(lldb) expr data.i
(lldb) memory read --size 1 --count 4 --format x `&data`
```

### 查看位域

```bash
# GDB
(gdb) p flags
(gdb) p flags.flag1
(gdb) p flags.value
(gdb) p/t flags.value  # 以二进制显示
(gdb) x/4xb &flags

# LLDB
(lldb) frame variable flags
(lldb) expr flags.value
(lldb) memory read --size 1 --count 4 --format b `&flags`
```

### 修改位域

```bash
# GDB
(gdb) set var flags.value = 63
(gdb) x/4xb &flags

# LLDB
(lldb) expr flags.value = 63
(lldb) memory read --size 1 --count 4 --format x `&flags`
```

## Union 的应用场景

### 1. 类型转换/重新解释

```c
union FloatInt {
    float f;
    uint32_t i;
};

// 查看浮点数的位表示
union FloatInt fi;
fi.f = 3.14f;
printf("Float bits: 0x%08x\n", fi.i);
```

### 2. 字节序转换

```c
union Endian {
    uint32_t value;
    uint8_t bytes[4];
};

void print_endian() {
    union Endian e = {0x01020304};
    if (e.bytes[0] == 0x04) {
        printf("Little Endian\n");
    } else {
        printf("Big Endian\n");
    }
}
```

### 3. 变体类型（Tagged Union）

```c
enum Type { INT, FLOAT, STRING };

struct Variant {
    enum Type type;
    union {
        int i;
        float f;
        char *s;
    } value;
};
```

## 位域的应用场景

### 1. 硬件寄存器

```c
struct ControlRegister {
    unsigned int enable : 1;
    unsigned int mode : 2;
    unsigned int speed : 3;
    unsigned int reserved : 26;
};
```

### 2. 网络协议 (IP Header)

```c
struct IPHeader {
    uint8_t version : 4;        // IP 版本
    uint8_t ihl : 4;            // Header 长度
    uint8_t tos;                // 服务类型
    uint16_t total_length;      // 总长度
    uint16_t identification;    // 标识
    uint16_t flags : 3;         // 标志
    uint16_t fragment_offset : 13;  // 片偏移
    uint8_t ttl;                // 生存时间
    uint8_t protocol;           // 协议
    uint16_t checksum;          // 校验和
    uint32_t source_ip;         // 源IP
    uint32_t dest_ip;           // 目的IP
};
```

### 3. 文件权限

```c
struct Permissions {
    unsigned int read : 1;
    unsigned int write : 1;
    unsigned int execute : 1;
};
```

## 常见陷阱

### 1. Union 的未定义行为

```c
union Data d;
d.i = 42;
printf("%f\n", d.f);  // ✗ 未定义行为！只能读取最后写入的成员
```

### 2. 位域的可移植性

```c
struct Flags {
    unsigned int a : 1;
    unsigned int b : 1;
};
// ✗ 位的顺序因编译器而异（从左到右还是从右到左？）
```

### 3. 位域的对齐

```c
struct Mixed {
    char c;
    unsigned int flag : 1;  // 可能引入额外 padding
};
// sizeof 可能不是你期望的！
```

## 性能考虑

### Union

- **优点**: 零开销（与直接类型转换相同）
- **缺点**: 需要程序员手动追踪当前使用的成员

### 位域

- **优点**: 节省内存
- **缺点**:
  - 访问需要位操作（稍慢）
  - 无法取地址（`&flags.flag1` 是非法的）
  - 不能使用 `sizeof` 查询单个位域

## 扩展练习

### 1. 实现字节序转换函数

```c
uint32_t htonl(uint32_t hostlong) {
    // 主机字节序转网络字节序（大端）
    // 提示：使用 union
}
```

### 2. 解析 RGB 颜色

```c
union Color {
    uint32_t value;  // 0xAARRGGBB
    struct {
        uint8_t blue;
        uint8_t green;
        uint8_t red;
        uint8_t alpha;
    };
};
```

### 3. 实现位图（Bitmap）

```c
struct Bitmap {
    unsigned int bit0 : 1;
    unsigned int bit1 : 1;
    // ... 更多位
};
```

## 调试检查清单

- [ ] 验证 union 的大小等于最大成员
- [ ] 通过 union 观察字节序
- [ ] 查看位域的内存布局
- [ ] 修改位域并观察变化
- [ ] 理解位域的限制

## 关键要点

1. **Union**: 所有成员共享内存，节省空间
2. **大小端**: 可以用 union 观察字节序
3. **位域**: 压缩多个小值，常用于协议和寄存器
4. **可移植性**: Union 和位域的布局依赖编译器
5. **性能**: Union 无开销，位域略慢但节省内存

## 总结

完成本练习后，你应该掌握：

1. ✅ Union 的内存共享机制
2. ✅ 使用 union 观察字节序
3. ✅ 位域的声明和使用
4. ✅ 位域的内存布局
5. ✅ 网络协议中的位域应用
6. ✅ Union 和位域的限制

Union 和位域是底层编程的重要工具！
