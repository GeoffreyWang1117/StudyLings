# 异步工具函数库

本框架提供了一个实用的异步编程工具库，位于 `src/utils/async-helpers.ts`。

## 使用方法

```typescript
import { delay, withTimeout, retry } from './src/utils/async-helpers';
```

## API 文档

### delay

延迟指定的毫秒数。

```typescript
function delay(ms: number): Promise<void>
```

**示例**：

```typescript
await delay(1000); // 等待 1 秒
console.log('1 秒后执行');
```

---

### withTimeout

为 Promise 添加超时控制。

```typescript
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutError?: Error
): Promise<T>
```

**参数**：
- `promise`: 要添加超时的 Promise
- `timeoutMs`: 超时时间（毫秒）
- `timeoutError`: 自定义超时错误（可选）

**示例**：

```typescript
const result = await withTimeout(
  fetchData(),
  5000,
  new Error('数据获取超时')
);
```

---

### retry

重试函数，支持指定重试次数和延迟。

```typescript
function retry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries: number;
    delay?: number;
    onRetry?: (error: Error, attempt: number) => void;
  }
): Promise<T>
```

**参数**：
- `fn`: 要重试的异步函数
- `options.maxRetries`: 最大重试次数
- `options.delay`: 重试间隔（毫秒，可选）
- `options.onRetry`: 重试时的回调（可选）

**示例**：

```typescript
const result = await retry(() => unstableAPI(), {
  maxRetries: 3,
  delay: 1000,
  onRetry: (error, attempt) => {
    console.log(`重试第 ${attempt} 次:`, error.message);
  },
});
```

---

### limitConcurrency

限制并发执行的任务数量。

```typescript
function limitConcurrency<T>(
  tasks: (() => Promise<T>)[],
  limit: number
): Promise<T[]>
```

**参数**：
- `tasks`: 任务函数数组
- `limit`: 最大并发数

**示例**：

```typescript
const tasks = urls.map(url => () => fetch(url));
const results = await limitConcurrency(tasks, 3); // 最多同时 3 个请求
```

---

### batchProcess

将数组分批处理。

```typescript
function batchProcess<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  batchSize: number
): Promise<R[]>
```

**参数**：
- `items`: 要处理的项目数组
- `processor`: 处理单个项目的函数
- `batchSize`: 每批的大小

**示例**：

```typescript
const results = await batchProcess(
  userIds,
  async (id) => fetchUser(id),
  10 // 每批处理 10 个
);
```

---

### debounce

防抖函数，在事件触发 n 秒后才执行，如果 n 秒内又触发，则重新计时。

```typescript
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void
```

**示例**：

```typescript
const debouncedSearch = debounce((query: string) => {
  console.log('搜索:', query);
}, 300);

// 用户快速输入时，只会在停止输入 300ms 后执行一次
debouncedSearch('a');
debouncedSearch('ab');
debouncedSearch('abc'); // 只有这次会执行
```

---

### throttle

节流函数，在 n 秒内只执行一次。

```typescript
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void
```

**示例**：

```typescript
const throttledScroll = throttle(() => {
  console.log('滚动事件');
}, 200);

window.addEventListener('scroll', throttledScroll);
// 无论滚动多快，200ms 内只会触发一次
```

---

### AsyncQueue

异步任务队列，按顺序执行任务。

```typescript
class AsyncQueue {
  enqueue<T>(task: () => Promise<T>): Promise<T>
}
```

**示例**：

```typescript
const queue = new AsyncQueue();

queue.enqueue(() => task1());
queue.enqueue(() => task2());
queue.enqueue(() => task3());

// 任务会按顺序执行，即使它们被同时添加
```

---

### memoizeAsync

缓存异步函数的结果。

```typescript
function memoizeAsync<T extends (...args: any[]) => Promise<any>>(
  fn: T
): T
```

**示例**：

```typescript
const cachedFetch = memoizeAsync(async (url: string) => {
  return await fetch(url);
});

await cachedFetch('/api/user/1'); // 实际请求
await cachedFetch('/api/user/1'); // 使用缓存
```

---

### poll

轮询函数，直到条件满足或超时。

```typescript
function poll<T>(
  fn: () => Promise<T>,
  options: {
    interval: number;
    timeout?: number;
    validate?: (result: T) => boolean;
  }
): Promise<T>
```

**参数**：
- `fn`: 要轮询的函数
- `options.interval`: 轮询间隔（毫秒）
- `options.timeout`: 超时时间（可选）
- `options.validate`: 验证结果的函数（可选）

**示例**：

```typescript
const result = await poll(
  () => checkJobStatus(jobId),
  {
    interval: 1000,     // 每秒检查一次
    timeout: 30000,     // 30 秒超时
    validate: (status) => status === 'completed',
  }
);
```

---

### promisify

将 callback 风格的函数转换为 Promise。

```typescript
function promisify<T>(
  fn: (callback: (error: Error | null, result?: T) => void) => void
): () => Promise<T>
```

**示例**：

```typescript
// 老式 callback 函数
function readFile(callback: (err: Error | null, data?: string) => void) {
  // ...
}

// 转换为 Promise
const readFileAsync = promisify(readFile);

// 现在可以使用 async/await
const data = await readFileAsync();
```

## 使用场景

### 1. API 请求超时

```typescript
const data = await withTimeout(
  fetch('/api/data'),
  5000
);
```

### 2. 不稳定服务重试

```typescript
const result = await retry(
  () => unstableService(),
  { maxRetries: 3, delay: 1000 }
);
```

### 3. 限制并发请求

```typescript
const results = await limitConcurrency(
  urls.map(url => () => fetch(url)),
  5 // 最多 5 个并发
);
```

### 4. 用户输入防抖

```typescript
const debouncedSearch = debounce(
  (query) => searchAPI(query),
  300
);

input.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

### 5. 滚动事件节流

```typescript
const throttledUpdate = throttle(
  () => updateVisibleItems(),
  100
);

window.addEventListener('scroll', throttledUpdate);
```

### 6. 轮询任务状态

```typescript
const finalStatus = await poll(
  () => getTaskStatus(taskId),
  {
    interval: 2000,
    timeout: 60000,
    validate: (status) => status.isDone,
  }
);
```

## 最佳实践

1. **选择合适的工具**：根据具体场景选择合适的函数
2. **设置合理的超时**：避免无限等待
3. **限制重试次数**：防止无限重试
4. **控制并发数**：避免资源耗尽
5. **缓存适当的结果**：减少重复计算

## 扩展学习

完成框架练习后，尝试：

1. 阅读这些工具函数的源码
2. 理解每个函数的实现原理
3. 根据自己的需求修改或扩展
4. 在实际项目中使用这些工具

这些工具函数都是异步编程的常见模式，掌握它们将大大提高你的开发效率！
