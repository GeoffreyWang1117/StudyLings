# Async Learnings 🚀

一个类似 [rustlings](https://github.com/rust-lang/rustlings) 的 TypeScript 异步编程学习框架。

通过由浅入深的练习题，帮助你掌握 JavaScript/TypeScript 的异步编程。

## 特点

- 📚 **循序渐进**: 从基础概念到实战应用，30 个精心设计的练习
- 🔄 **实时反馈**: 修改代码后自动运行测试，即时查看结果
- 💡 **提示系统**: 每个练习都有提示，帮助你找到解决方案
- 📖 **完整答案**: 提供所有练习的参考答案
- 🛠️ **工具库**: 包含常用异步编程工具函数
- 📊 **进度追踪**: 自动保存学习进度
- 🎨 **友好界面**: 彩色输出和清晰的错误信息
- 📝 **详细文档**: 包含学习指南、概念解析等

## 安装

```bash
# 安装依赖
npm install
```

## 快速开始

### 推荐方式：监控模式

```bash
npm run watch
```

这会启动监控模式：
- 自动定位到第一个未完成的练习
- 显示练习提示
- 监控文件变化，保存后自动运行测试
- 通过后自动进入下一个练习

### 其他命令

```bash
# 查看所有练习和进度
npm run list

# 运行当前练习（或指定练习）
npm run run
npm run run 01_intro

# 验证所有练习
npm run verify

# 显示当前练习的提示
npm run hint

# 查看当前练习的答案
npm run solution

# 跳到下一个练习（如果当前练习太难）
npm run next

# 重置学习进度
npm run reset
```

## 学习路径

### 1️⃣ 基础概念 (01_basics)

- **01_intro**: 理解同步与异步的区别
- **02_callback**: 回调函数的基本用法
- **03_callback_hell**: 体验回调地狱的问题

### 2️⃣ Promise 基础 (02_promises)

- **04_promise_intro**: 创建和使用 Promise
- **05_promise_then**: 使用 `.then()` 处理成功结果
- **06_promise_catch**: 使用 `.catch()` 处理错误
- **07_promise_chain**: Promise 链式调用
- **08_promise_all**: 并行执行多个 Promise
- **09_promise_race**: Promise 竞速

### 3️⃣ async/await (03_async_await)

- **10_async_intro**: async 函数基础
- **11_await_basic**: await 的基本用法
- **12_async_sequential**: 顺序执行异步操作
- **13_async_parallel**: 使用 Promise.all 并行执行

### 4️⃣ 错误处理 (04_error_handling)

- **14_try_catch**: 使用 try/catch 处理异步错误
- **15_error_propagation**: 理解错误传播
- **16_finally**: finally 块的使用

### 5️⃣ 并发控制 (05_concurrent)

- **17_concurrent_limit**: 限制并发数量
- **18_promise_allsettled**: 等待所有 Promise 完成
- **19_retry_mechanism**: 实现重试机制
- **20_timeout**: 为异步操作添加超时控制

### 6️⃣ 进阶主题 (06_advanced)

- **21_event_loop**: 理解 Event Loop 和执行顺序
- **22_async_iterator**: 使用异步迭代器
- **23_real_api**: 真实 API 调用场景
- **24_debounce_throttle**: 实现防抖和节流
- **25_async_queue**: 实现异步任务队列

### 7️⃣ 实战应用 (07_applications)

- **26_http_client**: 封装 HTTP 客户端，应用缓存、重试、超时等技术
- **27_connection_pool**: 实现数据库连接池，管理有限资源
- **28_file_processor**: 批量处理文件，控制并发和进度
- **29_task_scheduler**: 实现任务调度器，支持定时和依赖
- **30_rate_limiter**: 实现限流器，控制请求频率

## 学习建议

1. **按顺序完成练习**: 每个练习都建立在前面的基础上
2. **先思考后编码**: 阅读练习说明和提示，理解要求后再动手
3. **使用监控模式**: `npm run watch` 提供最好的学习体验
4. **不要害怕查看提示**: 如果卡住了，使用 `npm run hint` 获取帮助
5. **先尝试后看答案**: 尽量自己完成，实在卡住再用 `npm run solution`
6. **实验和探索**: 通过练习后，可以修改代码进行实验

## 练习格式

每个练习文件都包含：

```typescript
// 练习说明
// 解释这个练习要学习的概念

// 一些辅助函数（已实现）

// TODO: 你需要完成的代码
function yourTask() {
  // 在这里实现代码
  // 提示：...
}

// 测试代码（已实现）
```

## 如何判断练习完成

练习通过的条件：
1. 删除或完成所有 `TODO` 标记
2. 代码能够成功运行（退出码为 0）
3. 输出符合预期

## 常见问题

### Q: 如何跳过某个练习？

A: 使用 `npm run next` 跳到下一个练习。但建议先尝试完成当前练习。

### Q: 可以修改测试代码吗？

A: 建议不要修改测试代码，这样可以确保你正确理解了概念。

### Q: 进度保存在哪里？

A: 进度保存在项目根目录的 `.progress.json` 文件中。

### Q: 如何重新开始？

A: 使用 `npm run reset` 重置进度，或手动删除 `.progress.json` 文件。

### Q: 答案在哪里？

A: 所有练习的答案都在 `solutions/` 目录中，使用 `npm run solution` 查看。

## 项目结构

```
.
├── exercises/              # 练习题目录
│   ├── 01_basics/         # 基础概念
│   ├── 02_promises/       # Promise 基础
│   ├── 03_async_await/    # async/await
│   ├── 04_error_handling/ # 错误处理
│   ├── 05_concurrent/     # 并发控制
│   ├── 06_advanced/       # 进阶主题
│   └── 07_applications/   # 实战应用
├── solutions/             # 所有练习的答案
│   └── (同 exercises 结构)
├── docs/                  # 文档目录
│   ├── GUIDE.md          # 详细学习指南
│   ├── SOLUTIONS.md      # 答案使用说明
│   └── UTILS.md          # 工具函数文档
├── src/                   # 框架核心代码
│   ├── cli.ts            # 命令行接口
│   ├── config.ts         # 练习配置
│   ├── progress.ts       # 进度管理
│   ├── runner.ts         # 练习运行器
│   ├── types.ts          # 类型定义
│   ├── ui.ts             # 用户界面
│   ├── watcher.ts        # 文件监控
│   └── utils/            # 工具函数库
│       └── async-helpers.ts
├── package.json
├── tsconfig.json
└── README.md
```

## 文档

- **[学习指南 (GUIDE.md)](docs/GUIDE.md)**: 详细的异步编程概念解析、常见模式、最佳实践
- **[答案说明 (SOLUTIONS.md)](docs/SOLUTIONS.md)**: 如何使用和学习参考答案
- **[工具函数 (UTILS.md)](docs/UTILS.md)**: 实用的异步编程工具函数库
- **[快速参考 (CHEATSHEET.md)](docs/CHEATSHEET.md)**: 异步编程速查表
- **[常见错误 (COMMON_MISTAKES.md)](docs/COMMON_MISTAKES.md)**: 避免常见陷阱

## 工具函数库

项目包含一个实用的异步编程工具库 (`src/utils/async-helpers.ts`)，提供：

- `delay`: 延迟函数
- `withTimeout`: 超时控制
- `retry`: 重试机制
- `limitConcurrency`: 限制并发数
- `debounce/throttle`: 防抖和节流
- `AsyncQueue`: 异步队列
- `memoizeAsync`: 结果缓存
- `poll`: 轮询函数
- 更多...

详见 [工具函数文档](docs/UTILS.md)

## 实战示例

`examples/` 目录包含真实世界的异步编程示例：

1. **批量 API 请求客户端**: 并发控制、重试、超时
2. **文件下载器**: 并行下载、进度追踪
3. **网页爬虫**: 队列管理、去重、缓存

详见 [实战示例文档](examples/README.md)

## 贡献

欢迎提交 Issue 和 Pull Request！

如果你有好的练习想法或发现问题，请随时提出。

详见 [贡献指南](CONTRIBUTING.md)

## 许可

MIT

## 致谢

灵感来自 [rustlings](https://github.com/rust-lang/rustlings)

---

开始你的异步编程之旅吧！运行 `npm run watch` 开始学习 🎓
