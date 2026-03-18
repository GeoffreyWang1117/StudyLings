# TypeScript 异步编程快速参考

## 基础概念

### 回调函数

```typescript
function fetchData(callback: (data: string) => void) {
  setTimeout(() => callback('数据'), 1000);
}

fetchData((data) => console.log(data));
```

### Promise

```typescript
// 创建
const promise = new Promise((resolve, reject) => {
  if (success) resolve(value);
  else reject(error);
});

// 使用
promise
  .then(value => { /* 成功 */ })
  .catch(error => { /* 失败 */ })
  .finally(() => { /* 总是执行 */ });
```

### async/await

```typescript
async function fetchData() {
  try {
    const data = await someAsyncOperation();
    return data;
  } catch (error) {
    console.error(error);
  }
}
```

## 常用模式

### 1. 串行执行

```typescript
async function sequential() {
  const a = await task1();
  const b = await task2(a);
  const c = await task3(b);
  return c;
}
```

### 2. 并行执行

```typescript
async function parallel() {
  const [a, b, c] = await Promise.all([
    task1(),
    task2(),
    task3(),
  ]);
  return { a, b, c };
}
```

### 3. 超时控制

```typescript
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('超时')), ms)
  );
  return Promise.race([promise, timeout]);
}

// 使用
await withTimeout(fetchData(), 5000);
```

### 4. 重试机制

```typescript
async function retry<T>(
  fn: () => Promise<T>,
  retries: number
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0) return retry(fn, retries - 1);
    throw error;
  }
}

// 使用
await retry(() => unstableAPI(), 3);
```

### 5. 限制并发

```typescript
async function limitConcurrency<T>(
  tasks: (() => Promise<T>)[],
  limit: number
): Promise<T[]> {
  const results: T[] = [];
  const executing: Promise<void>[] = [];

  for (const task of tasks) {
    const p = task().then(r => results.push(r));
    executing.push(p);

    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(executing.findIndex(x => x === p), 1);
    }
  }

  await Promise.all(executing);
  return results;
}
```

### 6. 防抖

```typescript
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
) {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// 使用
const debouncedSearch = debounce(search, 300);
```

### 7. 节流

```typescript
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
) {
  let lastCall = 0;
  return (...args: Parameters<T>) => {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      fn(...args);
    }
  };
}

// 使用
const throttledScroll = throttle(onScroll, 100);
```

### 8. 轮询

```typescript
async function poll<T>(
  fn: () => Promise<T>,
  interval: number,
  maxAttempts?: number
): Promise<T> {
  let attempts = 0;

  while (true) {
    try {
      return await fn();
    } catch (error) {
      attempts++;
      if (maxAttempts && attempts >= maxAttempts) throw error;
      await new Promise(r => setTimeout(r, interval));
    }
  }
}
```

## Promise 静态方法

```typescript
// Promise.all - 全部成功才成功
const results = await Promise.all([p1, p2, p3]);

// Promise.race - 返回最快的结果
const fastest = await Promise.race([p1, p2, p3]);

// Promise.allSettled - 等待全部完成（不管成功失败）
const results = await Promise.allSettled([p1, p2, p3]);
// [{status: 'fulfilled', value: ...}, {status: 'rejected', reason: ...}]

// Promise.any - 任一成功即成功
const first = await Promise.any([p1, p2, p3]);

// Promise.resolve - 创建已解决的 Promise
const p = Promise.resolve(value);

// Promise.reject - 创建已拒绝的 Promise
const p = Promise.reject(error);
```

## 错误处理

### try/catch

```typescript
async function handleErrors() {
  try {
    await riskyOperation();
  } catch (error) {
    console.error(error);
  } finally {
    // 清理资源
  }
}
```

### .catch()

```typescript
promise
  .then(result => process(result))
  .catch(error => console.error(error));
```

### 错误传播

```typescript
async function chain() {
  try {
    const a = await step1(); // 如果失败，后续不执行
    const b = await step2(a);
    const c = await step3(b);
    return c;
  } catch (error) {
    // 捕获任何步骤的错误
    console.error('操作失败:', error);
  }
}
```

## Event Loop

### 执行顺序

```typescript
console.log('1'); // 同步 - 立即执行

setTimeout(() => console.log('2'), 0); // 宏任务 - 最后

Promise.resolve().then(() => console.log('3')); // 微任务 - 第三

console.log('4'); // 同步 - 第二

// 输出: 1, 4, 3, 2
```

### 微任务 vs 宏任务

**微任务**（优先级高）：
- `Promise.then/catch/finally`
- `queueMicrotask()`
- `MutationObserver`

**宏任务**（优先级低）：
- `setTimeout/setInterval`
- `setImmediate` (Node.js)
- I/O 操作
- UI 渲染

## 异步迭代器

```typescript
async function* asyncGenerator() {
  yield await fetch1();
  yield await fetch2();
  yield await fetch3();
}

// 使用
for await (const item of asyncGenerator()) {
  console.log(item);
}
```

## 常见陷阱

### ❌ 忘记 await

```typescript
// 错误
async function wrong() {
  const result = asyncOperation(); // 返回 Promise，不是值
  console.log(result); // Promise { <pending> }
}

// 正确
async function correct() {
  const result = await asyncOperation();
  console.log(result); // 实际的值
}
```

### ❌ 不必要的串行

```typescript
// 慢 - 串行执行
async function slow() {
  const a = await fetch1(); // 100ms
  const b = await fetch2(); // 100ms
  return [a, b]; // 总耗时 200ms
}

// 快 - 并行执行
async function fast() {
  const [a, b] = await Promise.all([
    fetch1(),
    fetch2(),
  ]);
  return [a, b]; // 总耗时 100ms
}
```

### ❌ 忽略错误处理

```typescript
// 危险
async function dangerous() {
  await riskyOperation(); // 如果失败会导致未捕获的异常
}

// 安全
async function safe() {
  try {
    await riskyOperation();
  } catch (error) {
    console.error('操作失败:', error);
  }
}
```

### ❌ forEach 中使用 await

```typescript
// 不会等待
array.forEach(async (item) => {
  await process(item); // 不会按预期工作
});

// 正确 - 串行
for (const item of array) {
  await process(item);
}

// 正确 - 并行
await Promise.all(array.map(item => process(item)));
```

## 性能优化

### 1. 避免过度并发

```typescript
// 不好 - 可能同时发起 1000 个请求
await Promise.all(items.map(fetchItem));

// 好 - 限制并发数为 5
await limitConcurrency(
  items.map(item => () => fetchItem(item)),
  5
);
```

### 2. 缓存结果

```typescript
const cache = new Map();

async function cachedFetch(url: string) {
  if (cache.has(url)) return cache.get(url);

  const data = await fetch(url);
  cache.set(url, data);
  return data;
}
```

### 3. 尽早启动异步操作

```typescript
// 不好
async function slow() {
  const a = await fetch1();
  const b = await fetch2(); // 等 fetch1 完成才开始
  return process(a, b);
}

// 好
async function fast() {
  const p1 = fetch1(); // 立即开始
  const p2 = fetch2(); // 立即开始
  const a = await p1;
  const b = await p2;
  return process(a, b);
}
```

## 调试技巧

### 1. 添加日志

```typescript
async function debugAsync() {
  console.log('开始');
  const result = await operation();
  console.log('完成:', result);
  return result;
}
```

### 2. 使用命名函数

```typescript
// 不好 - 匿名函数难以追踪
promise.then(data => process(data));

// 好 - 命名函数便于调试
promise.then(function processData(data) {
  return process(data);
});
```

### 3. 添加超时避免卡死

```typescript
const result = await withTimeout(
  longRunningOperation(),
  10000 // 10 秒超时
);
```

## 快速决策树

**需要顺序执行？**
→ 使用 `await` 串行

**操作独立且需要全部成功？**
→ 使用 `Promise.all()`

**只需最快的结果？**
→ 使用 `Promise.race()`

**需要全部完成（不管成败）？**
→ 使用 `Promise.allSettled()`

**需要限制并发数？**
→ 实现并发控制函数

**需要重试？**
→ 实现重试函数

**需要超时控制？**
→ 使用 `Promise.race()` + `setTimeout`

**频繁触发的事件？**
→ 使用防抖或节流

---

**提示**: 收藏此页面作为日常开发参考！
