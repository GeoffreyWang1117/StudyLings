# Exercise 3: 解决方案

## 自定义 GDB 命令：遍历链表

```python
# list_commands.py
import gdb

class PrintListCommand(gdb.Command):
    """打印整个链表"""

    def __init__(self):
        super(PrintListCommand, self).__init__("print-list", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        # 获取链表头
        try:
            head = gdb.parse_and_eval(arg)
        except:
            print("用法: print-list <list_head_variable>")
            return

        count = 0
        current = head
        print(f"Linked List Contents:")

        while current != 0:
            data = current['data']
            print(f"  Node {count}: data = {data}")

            current = current['next']
            count += 1

            if count > 100:  # 防止无限循环
                print("  ... (too many nodes)")
                break

        print(f"Total nodes: {count}")

PrintListCommand()
```

## 使用自定义命令

```bash
(gdb) source list_commands.py
(gdb) break main
(gdb) run
(gdb) next
(gdb) next
(gdb) next  # 创建链表后

(gdb) print-list head
Linked List Contents:
  Node 0: data = 1
  Node 1: data = 2
  Node 2: data = 3
Total nodes: 3
```

## Pretty Printer 完整版

```python
# list_printer.py
import gdb

class LinkedListPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        if self.val == 0:
            return "NULL"

        nodes = []
        current = self.val
        count = 0

        while current != 0 and count < 10:
            data = int(current['data'])
            nodes.append(str(data))
            current = current['next']
            count += 1

        if current != 0:
            nodes.append("...")

        return "List: " + " -> ".join(nodes)

def lookup_type(val):
    if val.type.code == gdb.TYPE_CODE_PTR:
        target_type = val.type.target()
        if str(target_type.tag) == 'Node':
            return LinkedListPrinter(val)
    return None

gdb.pretty_printers.append(lookup_type)
```

使用:
```bash
(gdb) source list_printer.py
(gdb) print head
$1 = List: 1 -> 2 -> 3
```

## Python 调试脚本示例

```python
# debug_script.py
import gdb

# 自动化调试会话
gdb.execute("file ./python_pretty")
gdb.execute("break main")
gdb.execute("run")

# 单步执行到链表创建后
for _ in range(3):
    gdb.execute("next")

# 获取并打印 head
head = gdb.parse_and_eval("head")
print(f"Head pointer: {head}")

# 遍历链表
current = head
while current != 0:
    data = current['data']
    print(f"Node data: {data}")
    current = current['next']

gdb.execute("continue")
```

运行:
```bash
gdb -x debug_script.py
```

## LLDB Python 脚本

LLDB 也支持 Python:
```python
# lldb_script.py
import lldb

def traverse_list(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    head = frame.FindVariable("head")

    current = head
    count = 0

    while current.GetValueAsUnsigned() != 0:
        data = current.GetChildMemberWithName("data")
        print(f"Node {count}: {data.GetValue()}")

        current = current.GetChildMemberWithName("next")
        count += 1

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f lldb_script.traverse_list traverse-list')
```

## 高级技巧

1. **条件断点与 Python**
```python
class ConditionalBreak(gdb.Breakpoint):
    def stop(self):
        # 自定义停止逻辑
        item = gdb.parse_and_eval("item")
        return item > 5
```

2. **自动化测试**
```python
# 在断点处验证值
gdb.execute("break calculate")
gdb.execute("run")
result = gdb.parse_and_eval("result")
assert result == 42, f"Expected 42, got {result}"
```

3. **性能分析**
```python
import time

class TimingBreakpoint(gdb.Breakpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.times = []

    def stop(self):
        self.times.append(time.time())
        return False

    def report(self):
        if len(self.times) > 1:
            intervals = [self.times[i+1] - self.times[i]
                        for i in range(len(self.times)-1)]
            print(f"Average: {sum(intervals)/len(intervals):.6f}s")
```

## 总结

Python 扩展让调试器变得更强大：
- 自定义命令简化重复操作
- Pretty printers 改善数据可视化
- 自动化脚本实现复杂调试流程
- 性能分析和测试验证
