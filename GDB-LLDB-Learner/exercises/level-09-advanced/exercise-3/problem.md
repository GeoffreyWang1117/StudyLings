# Exercise 3: Python 脚本和自定义命令

## 目标
学习使用 Python 扩展调试器功能，创建自定义命令和 pretty printers。

## 任务
1. 编写自定义 GDB 命令遍历链表
2. 创建链表的 pretty printer
3. 使用 Python 脚本自动化调试任务

## Python Pretty Printer 示例

创建文件 `list_printer.py`:
```python
import gdb

class NodePrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        data = self.val['data']
        next_ptr = self.val['next']
        return f"Node(data={data}, next={next_ptr})"

    def children(self):
        yield 'data', self.val['data']
        yield 'next', self.val['next']

def lookup_function(val):
    if str(val.type) == 'struct Node *':
        return NodePrinter(val.dereference())
    return None

gdb.pretty_printers.append(lookup_function)
```

## 使用
```bash
(gdb) source list_printer.py
(gdb) print head
Node(data=1, next=0x...)
```
