# TypeScript 异步编程学习指南

## 目录

1. [什么是异步编程](#什么是异步编程)
2. [核心概念](#核心概念)
3. [学习路线图](#学习路线图)
4. [常见模式](#常见模式)
5. [最佳实践](#最佳实践)
6. [调试技巧](#调试技巧)

## 什么是异步编程

### 同步 vs 异步

**同步代码**按顺序执行，每一行代码都会等待上一行完成：

```typescript
console.log('1');
console.log('2');
console.log('3');
// 输出: 1, 2, 3
```

**异步代码**不会阻塞后续代码的执行：

```typescript
console.log('1');
setTimeout(() => console.log('2'), 1000);
console.log('3');
// 输出: 1, 3, 2
```

### 为什么需要异步编程？

JavaScript 是单线程的。如果一个耗时操作（如网络请求）是同步的，整个程序都会被阻塞，无法响应用户操作。异步编程允许我们在等待耗时操作时继续执行其他代码。

## 核心概念

### 1. 回调函数（Callbacks）

最基本的异步模式，将一个函数作为参数传递给另一个函数：

```typescript
function fetchData(callback: (data: string) => void) {
  setTimeout(() => {
    callback('数据');
  }, 1000);
}

fetchData((data) => {
  console.log(data);
});
```

**缺点**：容易形成"回调地狱"，代码难以维护。

### 2. Promise

Promise 表示一个异步操作的最终完成或失败：

```typescript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('成功');
  }, 1000);
});

promise.then((result) => {
  console.log(result);
});
```

**三种状态**：
- Pending（进行中）
- Fulfilled（已成功）
- Rejected（已失败）

### 3. async/await

基于 Promise 的语法糖，让异步代码看起来像同步代码：

```typescript
async function fetchData() {
  const result = await someAsyncOperation();
  console.log(result);
}
```

## 学习路线图

```
1. 基础概念
   ├── 理解同步与异步
   ├── 回调函数
   └── 回调地狱问题

2. Promise
   ├── 创建 Promise
   ├── then/catch/finally
   ├── 链式调用
   ├── Promise.all()
   ├── Promise.race()
   └── Promise.allSettled()

3. async/await
   ├── async 函数
   ├── await 关键字
   ├── 顺序执行
   └── 并行执行

4. 错误处理
   ├── try/catch
   ├── 错误传播
   └── finally 块

5. 并发控制
   ├── 限制并发数
   ├── 重试机制
   └── 超时控制

6. 进阶主题
   ├── Event Loop
   ├── 异步迭代器
   ├── 防抖和节流
   └── 异步队列
```

## 常见模式

### 模式 1: 串行执行

按顺序执行多个异步操作：

```typescript
async function sequential() {
  const result1 = await operation1();
  const result2 = await operation2(result1);
  const result3 = await operation3(result2);
  return result3;
}
```

### 模式 2: 并行执行

同时执行多个独立的异步操作：

```typescript
async function parallel() {
  const [result1, result2, result3] = await Promise.all([
    operation1(),
    operation2(),
    operation3(),
  ]);
  return { result1, result2, result3 };
}
```

### 模式 3: 竞速

返回最先完成的结果：

```typescript
async function race() {
  const result = await Promise.race([
    fetchFromServer1(),
    fetchFromServer2(),
  ]);
  return result;
}
```

### 模式 4: 超时控制

```typescript
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('超时')), ms)
  );
  return Promise.race([promise, timeout]);
}
```

### 模式 5: 重试机制

```typescript
async function retry<T>(
  fn: () => Promise<T>,
  retries: number
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0) {
      return retry(fn, retries - 1);
    }
    throw error;
  }
}
```

## 最佳实践

### 1. 选择合适的模式

- **串行执行**：当后面的操作依赖前面的结果时
- **并行执行**：当操作之间相互独立时
- **竞速**：当只需要最快的结果时

### 2. 错误处理

始终处理可能的错误：

```typescript
// ✓ 好的做法
async function goodPractice() {
  try {
    const result = await riskyOperation();
    return result;
  } catch (error) {
    console.error('操作失败:', error);
    // 处理错误或重新抛出
  }
}

// ✗ 不好的做法
async function badPractice() {
  const result = await riskyOperation(); // 没有错误处理
  return result;
}
```

### 3. 避免忘记 await

```typescript
// ✗ 错误：忘记 await
async function wrong() {
  const result = asyncOperation(); // 返回 Promise，不是结果
  console.log(result); // 输出: Promise { <pending> }
}

// ✓ 正确
async function correct() {
  const result = await asyncOperation();
  console.log(result); // 输出实际结果
}
```

### 4. 合理使用并行

```typescript
// ✗ 性能差：顺序执行独立操作
async function slow() {
  const user = await fetchUser();      // 100ms
  const posts = await fetchPosts();    // 100ms
  const comments = await fetchComments(); // 100ms
  // 总耗时: 300ms
}

// ✓ 性能好：并行执行独立操作
async function fast() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ]);
  // 总耗时: 100ms
}
```

### 5. 清理资源

使用 finally 确保清理代码总是执行：

```typescript
async function withCleanup() {
  const resource = await acquireResource();
  try {
    await useResource(resource);
  } finally {
    await releaseResource(resource); // 总是会执行
  }
}
```

## 调试技巧

### 1. 使用 console.log 追踪执行顺序

```typescript
async function debug() {
  console.log('1: 开始');
  const result = await asyncOperation();
  console.log('2: 完成', result);
}
```

### 2. 捕获并记录错误

```typescript
async function withLogging() {
  try {
    const result = await operation();
    return result;
  } catch (error) {
    console.error('错误详情:', {
      message: error.message,
      stack: error.stack,
    });
    throw error;
  }
}
```

### 3. 使用 Promise.allSettled 查看所有结果

```typescript
const results = await Promise.allSettled([
  operation1(),
  operation2(),
  operation3(),
]);

results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`操作 ${index} 成功:`, result.value);
  } else {
    console.log(`操作 ${index} 失败:`, result.reason);
  }
});
```

### 4. 添加超时避免无限等待

```typescript
const result = await withTimeout(
  slowOperation(),
  5000 // 5秒超时
);
```

## Event Loop 详解

### 执行顺序

1. **同步代码**首先执行
2. **微任务**（Microtasks）：Promise.then、queueMicrotask
3. **宏任务**（Macrotasks）：setTimeout、setInterval、I/O

```typescript
console.log('1'); // 同步

setTimeout(() => console.log('2'), 0); // 宏任务

Promise.resolve().then(() => console.log('3')); // 微任务

console.log('4'); // 同步

// 输出顺序: 1, 4, 3, 2
```

### 理解微任务 vs 宏任务

- **微任务**在当前任务结束后立即执行
- **宏任务**在下一个 Event Loop 循环中执行

## 性能优化

### 1. 批量处理

```typescript
// 一次性处理多个操作，而不是逐个处理
async function batchProcess(items: string[]) {
  const results = await Promise.all(
    items.map(item => processItem(item))
  );
  return results;
}
```

### 2. 限制并发数

避免同时发起太多请求：

```typescript
async function limitConcurrency<T>(
  tasks: (() => Promise<T>)[],
  limit: number
): Promise<T[]> {
  const results: T[] = [];
  const executing: Promise<void>[] = [];

  for (const task of tasks) {
    const promise = task().then(result => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(executing.findIndex(p => p === promise), 1);
    }
  }

  await Promise.all(executing);
  return results;
}
```

### 3. 缓存结果

```typescript
const cache = new Map();

async function cachedFetch(url: string) {
  if (cache.has(url)) {
    return cache.get(url);
  }

  const result = await fetch(url);
  cache.set(url, result);
  return result;
}
```

## 总结

异步编程是 JavaScript/TypeScript 的核心能力。掌握它需要：

1. 理解基本概念（回调、Promise、async/await）
2. 学习常见模式（串行、并行、竞速等）
3. 遵循最佳实践（错误处理、性能优化）
4. 大量实践

通过完成本框架的 25 个练习，你将建立起扎实的异步编程基础！
