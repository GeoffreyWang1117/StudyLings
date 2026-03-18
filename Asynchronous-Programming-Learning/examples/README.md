# 实战示例

这个目录包含真实世界的异步编程示例，展示如何在实际项目中应用所学知识。

## 示例列表

### 1. 批量 API 请求客户端 (`01_batch_api_client.ts`)

**学习要点**：
- 并发控制
- 错误处理
- 重试机制
- 超时控制

**应用场景**：
- 批量数据导入
- 数据同步
- 批量更新操作

**运行**：
```bash
npx tsx examples/01_batch_api_client.ts
```

### 2. 文件下载器 (`02_file_downloader.ts`)

**学习要点**：
- 并行下载
- 进度追踪
- 资源管理

**应用场景**：
- 文件批量下载
- 媒体资源获取
- 数据备份

**运行**：
```bash
npx tsx examples/02_file_downloader.ts
```

### 3. 网页爬虫 (`03_web_scraper.ts`)

**学习要点**：
- 队列管理
- 深度优先/广度优先遍历
- 去重和缓存
- 爬虫礼仪（延迟、限速）

**应用场景**：
- 数据采集
- 内容聚合
- 网站监控

**运行**：
```bash
npx tsx examples/03_web_scraper.ts
```

## 学习建议

1. **先理解需求**：阅读代码注释，理解每个示例要解决的问题
2. **分析实现**：研究如何使用异步编程解决这些问题
3. **运行示例**：观察输出，理解执行流程
4. **修改实验**：尝试调整参数，观察行为变化
5. **扩展功能**：基于这些示例，添加新功能

## 从练习到实战

这些示例综合运用了练习中学到的概念：

| 练习章节 | 在实战中的应用 |
|---------|---------------|
| 基础概念 | 理解异步操作的本质 |
| Promise | 构建异步操作链 |
| async/await | 编写清晰的异步代码 |
| 错误处理 | 处理网络失败、超时等 |
| 并发控制 | 限制并发数、批量处理 |
| 进阶主题 | 队列、缓存、去重等模式 |

## 常见模式

这些示例展示了几种常见的异步编程模式：

### 1. 限制并发数

```typescript
async function limitConcurrency<T>(
  tasks: (() => Promise<T>)[],
  limit: number
): Promise<T[]>
```

**用途**：避免同时发起太多请求导致资源耗尽

### 2. 重试机制

```typescript
async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number
): Promise<T>
```

**用途**：处理临时性失败，提高成功率

### 3. 超时控制

```typescript
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T>
```

**用途**：避免无限等待，快速失败

### 4. 进度追踪

```typescript
await downloadFile(url, (progress) => {
  console.log(`进度: ${progress}%`);
});
```

**用途**：提供用户反馈，改善体验

### 5. 队列管理

```typescript
class TaskQueue {
  private queue: Array<() => Promise<any>> = [];

  async enqueue<T>(task: () => Promise<T>): Promise<T> {
    // 实现队列逻辑
  }
}
```

**用途**：控制任务执行顺序和并发

## 扩展挑战

尝试基于这些示例实现：

1. **为批量 API 客户端添加**：
   - 请求缓存
   - 批量重试失败的请求
   - 实时进度显示

2. **为文件下载器添加**：
   - 断点续传
   - 下载速度限制
   - 文件完整性验证

3. **为网页爬虫添加**：
   - 提取特定数据
   - 存储到数据库
   - 分布式爬取

## 实际项目参考

这些模式在真实项目中的应用：

- **API 客户端**：GraphQL 客户端、RESTful API SDK
- **下载工具**：IDM、aria2、wget
- **爬虫框架**：Puppeteer、Playwright、Scrapy

## 下一步

完成这些示例后，你可以：

1. 阅读开源项目的异步代码
2. 在自己的项目中应用这些模式
3. 探索更高级的异步模式（Streams、Workers 等）
4. 学习异步编程的性能优化

祝你编码愉快！🚀
