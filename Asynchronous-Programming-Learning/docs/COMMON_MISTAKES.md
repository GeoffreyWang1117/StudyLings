# 异步编程常见错误和陷阱

这个文档收集了学习和使用异步编程时最常见的错误和陷阱，以及如何避免它们。

## 目录

1. [忘记使用 await](#1-忘记使用-await)
2. [在循环中错误使用 async](#2-在循环中错误使用-async)
3. [不处理 Promise 拒绝](#3-不处理-promise-拒绝)
4. [过度串行化](#4-过度串行化)
5. [Promise 构造函数反模式](#5-promise-构造函数反模式)
6. [浮动 Promise](#6-浮动-promise)
7. [在 finally 中返回值](#7-在-finally-中返回值)
8. [误解 Promise.all 的行为](#8-误解-promiseall-的行为)
9. [async 函数中的返回陷阱](#9-async-函数中的返回陷阱)
10. [竞态条件](#10-竞态条件)

---

## 1. 忘记使用 await

### ❌ 错误

```typescript
async function getUserData() {
  const user = fetchUser(); // 忘记 await
  console.log(user.name); // TypeError: Cannot read property 'name' of undefined
  return user;
}
```

### ✅ 正确

```typescript
async function getUserData() {
  const user = await fetchUser(); // 正确使用 await
  console.log(user.name); // 正常工作
  return user;
}
```

### 为什么会出错？

不使用 `await`，`fetchUser()` 返回的是 `Promise` 对象，而不是实际的用户数据。

### 如何避免？

- 总是在 async 函数中的异步操作前使用 `await`
- 使用 TypeScript，它会在很多情况下警告你
- 如果你确实想要 Promise 对象，明确说明意图

---

## 2. 在循环中错误使用 async

### ❌ 错误：forEach 不等待

```typescript
async function processItems(items: string[]) {
  items.forEach(async (item) => {
    await process(item); // 不会等待！
  });
  console.log('完成'); // 会在处理之前打印
}
```

### ✅ 正确：使用 for...of 串行

```typescript
async function processItems(items: string[]) {
  for (const item of items) {
    await process(item); // 顺序处理
  }
  console.log('完成'); // 在所有处理之后打印
}
```

### ✅ 正确：使用 Promise.all 并行

```typescript
async function processItems(items: string[]) {
  await Promise.all(items.map(item => process(item)));
  console.log('完成'); // 在所有处理之后打印
}
```

### 为什么会出错？

`forEach`、`map` 等数组方法不理解异步操作，它们会立即返回，不等待回调完成。

### 如何避免？

- 串行处理：使用 `for...of`
- 并行处理：使用 `Promise.all()` + `map()`
- 永远不要在 `forEach` 中使用 `async`

---

## 3. 不处理 Promise 拒绝

### ❌ 错误

```typescript
async function fetchData() {
  const data = await riskyOperation(); // 如果失败，整个程序可能崩溃
  return data;
}
```

### ✅ 正确

```typescript
async function fetchData() {
  try {
    const data = await riskyOperation();
    return data;
  } catch (error) {
    console.error('获取数据失败:', error);
    throw error; // 或者返回默认值
  }
}
```

### 为什么会出错？

未捕获的 Promise 拒绝可能导致程序崩溃或出现难以调试的错误。

### 如何避免？

- 始终使用 try/catch 包裹可能失败的异步操作
- 或者使用 `.catch()` 处理错误
- 考虑使用全局的未处理拒绝处理器

```typescript
process.on('unhandledRejection', (error) => {
  console.error('未处理的 Promise 拒绝:', error);
});
```

---

## 4. 过度串行化

### ❌ 错误：不必要的串行

```typescript
async function fetchAllData() {
  const users = await fetchUsers();     // 等待 100ms
  const posts = await fetchPosts();     // 等待 100ms
  const comments = await fetchComments(); // 等待 100ms
  return { users, posts, comments };    // 总计 300ms
}
```

### ✅ 正确：并行执行

```typescript
async function fetchAllData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
  ]);
  return { users, posts, comments }; // 总计 100ms
}
```

### 为什么会出错？

顺序使用 `await` 会让操作串行执行，即使它们可以并行。

### 如何避免？

- 识别独立的异步操作
- 使用 `Promise.all()` 并行执行
- 只在操作有依赖关系时才串行

---

## 5. Promise 构造函数反模式

### ❌ 错误：不必要的包装

```typescript
async function getUser(id: number): Promise<User> {
  return new Promise(async (resolve, reject) => {
    try {
      const user = await fetchUser(id);
      resolve(user);
    } catch (error) {
      reject(error);
    }
  });
}
```

### ✅ 正确：直接返回

```typescript
async function getUser(id: number): Promise<User> {
  return await fetchUser(id);
  // 或者更简单：
  // return fetchUser(id);
}
```

### 为什么会出错？

async 函数已经返回 Promise，不需要再包装一层。

### 如何避免？

- 记住：async 函数总是返回 Promise
- 只在需要将回调转换为 Promise 时使用 Promise 构造函数
- 使用 `util.promisify()` 转换 Node.js 回调

---

## 6. 浮动 Promise

### ❌ 错误：启动但不等待

```typescript
function processData() {
  saveToDatabase(data); // 浮动的 Promise
  return 'Success'; // 可能在保存完成前返回
}
```

### ✅ 正确：明确等待或忽略

```typescript
async function processData() {
  await saveToDatabase(data); // 明确等待
  return 'Success';
}

// 或者明确不等待（如果这是你想要的）
function processDataAsync() {
  saveToDatabase(data).catch(console.error); // 至少处理错误
  return 'Success';
}
```

### 为什么会出错？

浮动的 Promise 可能在你不期望的时候完成，且错误可能不会被捕获。

### 如何避免？

- 始终 await 异步调用
- 如果确实想要"fire and forget"，至少添加 `.catch()` 处理错误
- 使用 ESLint 规则 `@typescript-eslint/no-floating-promises`

---

## 7. 在 finally 中返回值

### ❌ 错误

```typescript
async function process() {
  try {
    return await operation(); // 返回 'success'
  } catch (error) {
    return 'error';
  } finally {
    return 'done'; // 会覆盖之前的返回值！
  }
}
```

### ✅ 正确

```typescript
async function process() {
  try {
    return await operation();
  } catch (error) {
    return 'error';
  } finally {
    cleanup(); // 只做清理，不返回值
  }
}
```

### 为什么会出错？

`finally` 中的 return 会覆盖 try/catch 中的返回值或抛出的错误。

### 如何避免？

- 永远不要在 finally 块中使用 return
- finally 只用于清理资源
- ESLint 会警告这种情况

---

## 8. 误解 Promise.all 的行为

### ❌ 错误：以为会等待所有完成

```typescript
async function fetchAllWithErrors() {
  try {
    const results = await Promise.all([
      fetch1(), // 成功
      fetch2(), // 失败
      fetch3(), // 可能不会执行
    ]);
  } catch (error) {
    // 只能捕获第一个错误
    // fetch3 的结果丢失了
  }
}
```

### ✅ 正确：使用 Promise.allSettled

```typescript
async function fetchAllWithErrors() {
  const results = await Promise.allSettled([
    fetch1(),
    fetch2(),
    fetch3(),
  ]);

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      console.log(`任务 ${index} 成功:`, result.value);
    } else {
      console.log(`任务 ${index} 失败:`, result.reason);
    }
  });
}
```

### 为什么会出错？

`Promise.all()` 会在第一个拒绝时立即拒绝，其他 Promise 的结果会丢失。

### 如何避免？

- 需要全部成功才成功：使用 `Promise.all()`
- 需要所有结果（包括失败的）：使用 `Promise.allSettled()`
- 需要任一成功：使用 `Promise.any()`

---

## 9. async 函数中的返回陷阱

### ❌ 错误：返回 await 的 Promise

```typescript
async function getData() {
  try {
    return await fetchData(); // 多余的 await
  } catch (error) {
    console.error(error);
  }
}
```

### ✅ 正确：直接返回 Promise

```typescript
async function getData() {
  try {
    return fetchData(); // 不需要 await
  } catch (error) {
    console.error(error);
  }
}
```

### 但是注意！

如果需要在 try/catch 中捕获错误，**必须** 使用 await：

```typescript
async function getData() {
  try {
    return await fetchData(); // 这里 await 是必需的！
  } catch (error) {
    console.error(error);
    return defaultData;
  }
}
```

### 为什么？

- 在 async 函数的最后 return 时，await 通常是多余的
- 但在 try/catch 中，必须 await 才能捕获错误

---

## 10. 竞态条件

### ❌ 错误：不处理过时的请求

```typescript
let currentRequest = 0;

async function searchUsers(query: string) {
  const results = await api.search(query); // 可能很慢
  displayResults(results); // 可能显示过时的结果
}

// 用户快速输入：
searchUsers('a');   // 请求 1
searchUsers('ab');  // 请求 2
searchUsers('abc'); // 请求 3
// 如果请求 1 最慢，会覆盖请求 3 的结果！
```

### ✅ 正确：使用请求 ID

```typescript
let requestId = 0;

async function searchUsers(query: string) {
  const currentId = ++requestId;
  const results = await api.search(query);

  // 只显示最新请求的结果
  if (currentId === requestId) {
    displayResults(results);
  }
}
```

### ✅ 更好：使用 AbortController

```typescript
let abortController: AbortController | null = null;

async function searchUsers(query: string) {
  // 取消之前的请求
  if (abortController) {
    abortController.abort();
  }

  abortController = new AbortController();

  try {
    const results = await api.search(query, {
      signal: abortController.signal,
    });
    displayResults(results);
  } catch (error) {
    if (error.name === 'AbortError') {
      // 请求被取消，忽略
    } else {
      throw error;
    }
  }
}
```

### 为什么会出错？

多个异步操作可能以不同的顺序完成，导致显示过时的数据。

### 如何避免？

- 使用请求 ID 验证结果的时效性
- 使用 AbortController 取消过时的请求
- 考虑使用防抖减少请求数量

---

## 最佳实践总结

1. **总是处理错误**：使用 try/catch 或 .catch()
2. **识别并行机会**：独立操作用 Promise.all()
3. **不要在 forEach 中用 async**：使用 for...of 或 map + Promise.all
4. **明确 await**：需要值时 await，需要 Promise 时不要
5. **避免浮动 Promise**：要么 await，要么至少 .catch()
6. **使用 TypeScript**：它能捕获很多异步错误
7. **启用 ESLint 规则**：
   - `@typescript-eslint/no-floating-promises`
   - `@typescript-eslint/await-thenable`
   - `@typescript-eslint/no-misused-promises`

---

## 调试技巧

### 1. 添加日志追踪

```typescript
async function debugAsync() {
  console.log('开始');
  try {
    const result = await operation();
    console.log('成功:', result);
    return result;
  } catch (error) {
    console.error('失败:', error);
    throw error;
  }
}
```

### 2. 使用 Promise 检查工具

```typescript
// 检查是否是 Promise
if (value instanceof Promise) {
  console.warn('忘记 await 了吗？');
}
```

### 3. 设置超时避免永久等待

```typescript
const result = await withTimeout(operation(), 5000);
```

---

记住：最好的避免错误的方法是**理解异步编程的工作原理**，而不是死记硬背规则。

通过完成本项目的练习，你将建立对异步编程的深入理解！
