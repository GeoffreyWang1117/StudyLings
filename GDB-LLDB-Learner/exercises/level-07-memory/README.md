# Level 7: 内存和数据结构调试

## 学习目标

- 检查内存内容
- 调试数组和指针
- 分析内存布局
- 检测内存错误

## 核心命令

### GDB 命令
```bash
x/10x 0x400000          # 检查内存（十六进制）
x/10d &variable         # 检查内存（十进制）
x/s string_ptr          # 以字符串格式查看
print array[0]@10       # 打印数组的 10 个元素
print *pointer          # 解引用指针
print &variable         # 获取地址
```

### LLDB 命令
```bash
memory read -c 10 -fx 0x400000   # 检查内存（十六进制）
x/10x 0x400000                   # 也支持 GDB 语法
parray 10 array                  # 打印数组
p *pointer                       # 解引用指针
p &variable                      # 获取地址
```

## 内存格式说明

`x/Nfu addr` 格式：
- `N`: 显示数量
- `f`: 格式（x=十六进制, d=十进制, s=字符串, i=指令）
- `u`: 单位（b=字节, h=半字, w=字, g=双字）

示例：
```
x/10xw 0x400000    # 以十六进制显示 10 个字（word）
x/20xb 0x400000    # 以十六进制显示 20 个字节
x/s string_ptr     # 显示字符串
```
