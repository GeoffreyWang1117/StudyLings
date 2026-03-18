/**
 * 异步编程实用工具库
 *
 * 这个文件提供了一些常用的异步编程辅助函数
 * 学习者可以参考这些实现来理解异步模式
 */

/**
 * 延迟指定的毫秒数
 */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 为 Promise 添加超时控制
 */
export function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutError: Error = new Error(`操作超时（${timeoutMs}ms）`)
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(timeoutError), timeoutMs);
  });

  return Promise.race([promise, timeoutPromise]);
}

/**
 * 重试函数，支持指定重试次数和延迟
 */
export async function retry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries: number;
    delay?: number;
    onRetry?: (error: Error, attempt: number) => void;
  }
): Promise<T> {
  const { maxRetries, delay: retryDelay = 0, onRetry } = options;
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;

      if (attempt < maxRetries) {
        onRetry?.(error, attempt + 1);

        if (retryDelay > 0) {
          await delay(retryDelay);
        }
      }
    }
  }

  throw lastError!;
}

/**
 * 限制并发数量
 */
export async function limitConcurrency<T>(
  tasks: (() => Promise<T>)[],
  limit: number
): Promise<T[]> {
  const results: T[] = [];
  const executing: Promise<void>[] = [];

  for (const task of tasks) {
    const promise = task().then((result) => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(
        executing.findIndex((p) => p === promise),
        1
      );
    }
  }

  await Promise.all(executing);
  return results;
}

/**
 * 批量处理，将数组分批处理
 */
export async function batchProcess<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  batchSize: number
): Promise<R[]> {
  const results: R[] = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(batch.map(processor));
    results.push(...batchResults);
  }

  return results;
}

/**
 * 防抖函数
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout | null = null;

  return function (...args: Parameters<T>) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}

/**
 * 节流函数
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastCall = 0;

  return function (...args: Parameters<T>) {
    const now = Date.now();

    if (now - lastCall >= delay) {
      lastCall = now;
      fn(...args);
    }
  };
}

/**
 * 异步队列类
 */
export class AsyncQueue {
  private queue: Array<{
    task: () => Promise<any>;
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }> = [];
  private running: boolean = false;

  enqueue<T>(task: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject });

      if (!this.running) {
        this.processQueue();
      }
    });
  }

  private async processQueue(): Promise<void> {
    if (this.running || this.queue.length === 0) {
      return;
    }

    this.running = true;

    while (this.queue.length > 0) {
      const item = this.queue.shift();

      if (item) {
        try {
          const result = await item.task();
          item.resolve(result);
        } catch (error) {
          item.reject(error);
        }
      }
    }

    this.running = false;
  }
}

/**
 * 缓存 Promise 结果
 */
export function memoizeAsync<T extends (...args: any[]) => Promise<any>>(
  fn: T
): T {
  const cache = new Map<string, Promise<any>>();

  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const promise = fn(...args);
    cache.set(key, promise);

    return promise.catch((error) => {
      cache.delete(key);
      throw error;
    });
  }) as T;
}

/**
 * 轮询函数，直到条件满足或超时
 */
export async function poll<T>(
  fn: () => Promise<T>,
  options: {
    interval: number;
    timeout?: number;
    validate?: (result: T) => boolean;
  }
): Promise<T> {
  const { interval, timeout, validate = () => true } = options;
  const startTime = Date.now();

  while (true) {
    const result = await fn();

    if (validate(result)) {
      return result;
    }

    if (timeout && Date.now() - startTime > timeout) {
      throw new Error('轮询超时');
    }

    await delay(interval);
  }
}

/**
 * 将 callback 风格的函数转换为 Promise
 */
export function promisify<T>(
  fn: (callback: (error: Error | null, result?: T) => void) => void
): () => Promise<T> {
  return () =>
    new Promise((resolve, reject) => {
      fn((error, result) => {
        if (error) {
          reject(error);
        } else {
          resolve(result as T);
        }
      });
    });
}
