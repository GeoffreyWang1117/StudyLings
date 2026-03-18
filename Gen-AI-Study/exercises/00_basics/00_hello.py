"""
练习 00: Hello Genlings!

欢迎来到 Genlings - 生成式AI算法填空练习！

这是你的第一个练习。任务很简单：让程序打印出 "Hello, Genlings!"

在本项目中，你需要：
1. 找到标记为 TODO 的地方
2. 将 ___ 替换为正确的代码
3. 运行程序验证答案

提示：___ 表示需要你填写的空白处
"""


def greet():
    # TODO: 在下面的 print 语句中填入正确的字符串
    # 让程序打印 "Hello, Genlings!"
    message = ___  # 填入字符串 "Hello, Genlings!"
    print(message)
    return message


def main():
    result = greet()
    # 验证
    assert result == "Hello, Genlings!", f"期望 'Hello, Genlings!'，但得到 '{result}'"
    print("✓ 太棒了！你完成了第一个练习！")


if __name__ == "__main__":
    main()
