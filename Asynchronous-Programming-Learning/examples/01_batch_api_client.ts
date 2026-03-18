/**
 * 实战示例 1: 批量 API 请求客户端
 *
 * 这个示例展示如何：
 * - 批量处理 API 请求
 * - 限制并发数量
 * - 实现重试机制
 * - 处理错误和超时
 */

// 模拟 API 请求
async function fetchUser(id: number): Promise<{id: number; name: string}> {
  return new Promise((resolve, reject) => {
    const delay = Math.random() * 200 + 100;

    setTimeout(() => {
      // 10% 的失败率
      if (Math.random() < 0.1) {
        reject(new Error(`获取用户 ${id} 失败`));
      } else {
        resolve({ id, name: `User${id}` });
      }
    }, delay);
  });
}

// 超时控制
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('请求超时')), timeoutMs)
    ),
  ]);
}

// 重试机制
async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (i === maxRetries) throw error;
      console.log(`  重试 ${i + 1}/${maxRetries}...`);
      await new Promise(r => setTimeout(r, 100 * (i + 1))); // 指数退避
    }
  }
  throw new Error('不应该到达这里');
}

// 限制并发
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

// 批量 API 客户端
class BatchApiClient {
  private concurrencyLimit: number;
  private timeout: number;
  private retries: number;

  constructor(options: {
    concurrencyLimit?: number;
    timeout?: number;
    retries?: number;
  } = {}) {
    this.concurrencyLimit = options.concurrencyLimit || 5;
    this.timeout = options.timeout || 5000;
    this.retries = options.retries || 3;
  }

  async fetchUsers(userIds: number[]): Promise<{
    success: Array<{id: number; name: string}>;
    failed: Array<{id: number; error: string}>;
  }> {
    console.log(`开始批量获取 ${userIds.length} 个用户...`);
    console.log(`并发限制: ${this.concurrencyLimit}`);
    console.log(`超时: ${this.timeout}ms`);
    console.log(`重试次数: ${this.retries}\n`);

    const tasks = userIds.map(id => async () => {
      try {
        console.log(`获取用户 ${id}...`);

        const user = await retry(
          () => withTimeout(fetchUser(id), this.timeout),
          this.retries
        );

        console.log(`✓ 用户 ${id} 获取成功`);
        return { success: true, data: user };
      } catch (error: any) {
        console.log(`✗ 用户 ${id} 获取失败: ${error.message}`);
        return { success: false, id, error: error.message };
      }
    });

    const results = await limitConcurrency(tasks, this.concurrencyLimit);

    const success = results
      .filter((r: any) => r.success)
      .map((r: any) => r.data);

    const failed = results
      .filter((r: any) => !r.success)
      .map((r: any) => ({ id: r.id, error: r.error }));

    return { success, failed };
  }
}

// 使用示例
async function main() {
  const client = new BatchApiClient({
    concurrencyLimit: 3,
    timeout: 2000,
    retries: 2,
  });

  const userIds = Array.from({ length: 10 }, (_, i) => i + 1);

  const startTime = Date.now();
  const results = await client.fetchUsers(userIds);
  const duration = Date.now() - startTime;

  console.log('\n' + '='.repeat(50));
  console.log('结果统计');
  console.log('='.repeat(50));
  console.log(`成功: ${results.success.length}`);
  console.log(`失败: ${results.failed.length}`);
  console.log(`总耗时: ${duration}ms`);

  if (results.failed.length > 0) {
    console.log('\n失败的请求:');
    results.failed.forEach(f => {
      console.log(`  用户 ${f.id}: ${f.error}`);
    });
  }
}

main();
