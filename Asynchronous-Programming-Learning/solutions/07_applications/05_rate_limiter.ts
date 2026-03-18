// 练习 30: 限流器 (Rate Limiter) - 答案
//
// 实现一个限流器，控制 API 调用频率

interface RateLimiterConfig {
  maxRequests: number; // 最大请求数
  windowMs: number; // 时间窗口（毫秒）
  strategy?: 'fixed' | 'sliding'; // 策略
}

// 实现限流器
class RateLimiter {
  private maxRequests: number;
  private windowMs: number;
  private strategy: 'fixed' | 'sliding';
  private requests: number[] = []; // 请求时间戳
  private windowStart: number = Date.now();

  constructor(config: RateLimiterConfig) {
    this.maxRequests = config.maxRequests;
    this.windowMs = config.windowMs;
    this.strategy = config.strategy || 'sliding';
  }

  // 尝试执行请求
  async tryAcquire(): Promise<boolean> {
    const now = Date.now();

    if (this.strategy === 'fixed') {
      // 固定时间窗口策略
      // 如果当前时间超过窗口结束时间，重置窗口
      if (now >= this.windowStart + this.windowMs) {
        this.windowStart = now;
        this.requests = [];
      }

      // 检查是否超过限制
      if (this.requests.length < this.maxRequests) {
        this.requests.push(now);
        return true;
      }

      return false;
    } else {
      // 滑动时间窗口策略
      // 清理过期的请求记录
      this.requests = this.requests.filter(
        (time) => now - time < this.windowMs
      );

      // 检查是否超过限制
      if (this.requests.length < this.maxRequests) {
        this.requests.push(now);
        return true;
      }

      return false;
    }
  }

  // 执行带限流的函数
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    // 等待直到可以执行
    while (true) {
      const canProceed = await this.tryAcquire();

      if (canProceed) {
        // 执行函数并返回结果
        return await fn();
      }

      // 如果使用滑动窗口策略，计算需要等待的时间
      if (this.strategy === 'sliding' && this.requests.length > 0) {
        const oldestRequest = this.requests[0];
        const waitTime = this.windowMs - (Date.now() - oldestRequest);
        if (waitTime > 0) {
          await new Promise((resolve) => setTimeout(resolve, waitTime + 10));
        }
      } else if (this.strategy === 'fixed') {
        // 固定窗口策略，等待窗口重置
        const waitTime = this.windowStart + this.windowMs - Date.now();
        if (waitTime > 0) {
          await new Promise((resolve) => setTimeout(resolve, waitTime + 10));
        }
      } else {
        // 短暂等待后重试
        await new Promise((resolve) => setTimeout(resolve, 50));
      }
    }
  }

  // 获取当前状态
  getStatus() {
    const now = Date.now();
    const validRequests = this.requests.filter(
      (time) => now - time < this.windowMs
    );

    return {
      currentRequests: validRequests.length,
      maxRequests: this.maxRequests,
      remaining: Math.max(0, this.maxRequests - validRequests.length),
      resetAt: new Date(this.windowStart + this.windowMs),
    };
  }
}

// 模拟 API 调用
async function apiCall(id: number): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`API 响应 ${id}`);
    }, 100);
  });
}

// 测试代码
async function testRateLimiter() {
  console.log('测试 1: 固定窗口限流器');
  console.log('配置: 5 个请求/秒\n');

  const limiter1 = new RateLimiter({
    maxRequests: 5,
    windowMs: 1000,
    strategy: 'fixed',
  });

  const requests: Promise<any>[] = [];

  // 尝试发起 8 个请求
  for (let i = 1; i <= 8; i++) {
    requests.push(
      (async () => {
        const startTime = Date.now();
        const canProceed = await limiter1.tryAcquire();

        if (canProceed) {
          const result = await apiCall(i);
          const elapsed = Date.now() - startTime;
          console.log(`✓ 请求 ${i}: ${result} (等待 ${elapsed}ms)`);
        } else {
          console.log(`✗ 请求 ${i}: 被限流`);
        }

        const status = limiter1.getStatus();
        console.log(`  状态: ${status.currentRequests}/${status.maxRequests} (剩余: ${status.remaining})`);
      })()
    );
  }

  await Promise.all(requests);

  console.log('\n测试 2: 滑动窗口限流器');
  console.log('配置: 3 个请求/500ms\n');

  const limiter2 = new RateLimiter({
    maxRequests: 3,
    windowMs: 500,
    strategy: 'sliding',
  });

  // 快速发起 6 个请求
  for (let i = 1; i <= 6; i++) {
    limiter2
      .execute(async () => {
        const result = await apiCall(i);
        console.log(`✓ 请求 ${i}: ${result}`);
        return result;
      })
      .catch((error) => {
        console.log(`✗ 请求 ${i}: ${error.message}`);
      });

    // 小延迟
    await new Promise((r) => setTimeout(r, 50));
  }

  // 等待所有请求完成
  await new Promise((r) => setTimeout(r, 2000));

  console.log('\n✓ 所有测试完成');
}

testRateLimiter();
