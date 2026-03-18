# Exercise 3: 哈希表调试

## 学习目标

- 理解哈希表的内存结构
- 掌握链地址法冲突解决
- 学习如何分析哈希分布
- 调试哈希表的桶和链表

## 背景知识

### 哈希表结构

```c
typedef struct Entry {
    char *key;
    int value;
    struct Entry *next;  // 链地址法：指向下一个冲突项
} Entry;

typedef struct HashTable {
    Entry **buckets;     // 桶数组（指针数组）
    int size;            // 桶的数量
};
```

### 内存布局

```
HashTable
  └─ buckets[0] → Entry1 → Entry2 → NULL
     buckets[1] → NULL
     buckets[2] → Entry3 → NULL
     ...
     buckets[9] → Entry4 → Entry5 → Entry6 → NULL
```

## 任务

### 任务 1: 分析哈希函数

**目标**: 理解哈希函数如何将 key 映射到桶索引

**步骤**:
1. 在 `hash()` 函数上设置断点
2. 传入不同的 key，观察返回的索引值
3. 验证哈希算法：`hash = (hash << 5) + char`

**问题**:
- "apple" 映射到哪个桶？
- "banana" 和 "elderberry" 是否有冲突？
- 左移5位相当于乘以多少？

### 任务 2: 检查桶内链表

**目标**: 遍历每个桶的链表，查看冲突的解决

**步骤**:
1. 在程序运行后设置断点
2. 遍历 `table->buckets` 数组
3. 对于非空桶，遍历其链表

**问题**:
- 哪个桶有最多的条目？
- 打印 buckets[3] 的所有条目（如果有）
- 验证链表的完整性（是否正确终止于 NULL）

### 任务 3: 追踪插入过程

**目标**: 观察新条目如何插入到链表头部

**步骤**:
1. 在 `insert()` 函数上设置断点
2. 单步执行，观察：
   - 哈希值计算
   - Entry 分配
   - 链表头部插入（`entry->next = table->buckets[index]`）
3. 检查插入后的内存状态

**问题**:
- 新条目是插入链表头部还是尾部？
- 如果两个 key 哈希到同一个桶，它们的顺序是什么？

### 任务 4: 哈希分布分析

**目标**: 评估哈希函数的均匀性

**步骤**:
1. 运行程序，查看每个桶的条目数量
2. 计算最大负载和平均负载
3. 检查是否有空桶

**问题**:
- 5个条目分布在几个桶中？
- 最大的桶有几个条目？
- 这个哈希函数的均匀性如何？

## 编译和运行

```bash
make
./hashtable

# GDB
gdb ./hashtable

# LLDB
lldb ./hashtable
```

## 预期输出

```
=== 哈希表调试 ===

Hash distribution:
Bucket[X]: Y entries
...

任务:
1. 检查每个桶的链表
2. 验证哈希函数分布
3. 查找特定 key 的存储位置
```

## 提示

### 遍历所有桶

```bash
# GDB
set $i = 0
while $i < table->size
    printf "Bucket[%d]: ", $i
    set $e = table->buckets[$i]
    while $e != 0
        printf "%s=%d ", $e->key, $e->value
        set $e = $e->next
    end
    printf "\n"
    set $i = $i + 1
end
```

### 计算哈希值

```bash
# GDB
print hash("apple")
```

### 查看桶内容

```bash
# GDB
print table->buckets[3]
print table->buckets[3]->key
print table->buckets[3]->value
print table->buckets[3]->next
```

## 扩展挑战

1. **查找函数**: 实现一个 `find(table, key)` 函数，使用调试器验证
2. **冲突统计**: 计算有多少个桶有冲突（链表长度 > 1）
3. **自定义哈希**: 修改哈希函数，观察分布的变化
4. **性能分析**: 比较不同 TABLE_SIZE 下的性能

## 关键概念

- **哈希函数**: 将 key 映射到索引的函数
- **冲突**: 多个 key 映射到同一个索引
- **链地址法**: 使用链表存储冲突的条目
- **负载因子**: 条目数 / 桶数，影响性能
- **均匀分布**: 好的哈希函数应将 key 均匀分布到所有桶

## 常见问题

**Q: 为什么使用链表头部插入？**
A: O(1) 时间复杂度，不需要遍历到尾部

**Q: 如何检测哈希冲突？**
A: 检查桶的链表长度是否 > 1

**Q: TABLE_SIZE 为什么选择 10？**
A: 故意使用小值来制造冲突，便于学习

## 下一步

完成后，继续学习：
- Level 11: 多级指针（理解 `Entry **buckets`）
- Level 9: 自定义 Pretty Printer（可视化哈希表）
