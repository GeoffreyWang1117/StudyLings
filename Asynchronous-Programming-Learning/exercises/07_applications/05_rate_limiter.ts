// 练习 30: 限流器 (Rate Limiter)
//
// 【学习目标】
// 在这个练习中，你将实现一个 API 限流器，学习：
// 1. 固定窗口算法 - 在固定时间段内限制请求数
// 2. 滑动窗口算法 - 更平滑的限流策略
// 3. 自动等待 - 超过限制时等待而非拒绝
// 4. 流量控制 - 保护 API 不被过度调用
//
// 【核心概念】
// - 固定窗口：时间窗口到期后重置计数
//   - 优点：实现简单，重置清晰
//   - 缺点：窗口边界可能出现突发流量
// - 滑动窗口：持续滚动的时间窗口
//   - 优点：流量更平滑，限制更精确
//   - 缺点：需要记录每次请求时间
// - 等待策略：计算需要等待的时间，自动等待后执行
//
// 【实现提示】
// 1. tryAcquire()：尝试获取执行权限
//    - 固定窗口策略：
//      * 检查是否超过窗口结束时间，是则重置
//      * 检查当前窗口内请求数是否小于限制
//    - 滑动窗口策略：
//      * 清理过期记录（now - time >= windowMs）
//      * 检查有效请求数是否小于限制
//    - 未超限则添加记录，返回 true
// 2. execute()：执行带限流的函数
//    - 循环尝试获取权限
//    - 成功则执行函数
//    - 失败则计算等待时间并等待
//
// 【预期行为】
// - 固定窗口：每个时间窗口内最多执行 N 次
// - 滑动窗口：任意时间段内最多执行 N 次
// - 超过限制会自动等待
// - execute 方法保证最终执行

interface RateLimiterConfig {
  maxRequests: number; // 最大请求数
  windowMs: number; // 时间窗口（毫秒）
  strategy?: 'fixed' | 'sliding'; // 策略
}

// TODO: 实现限流器
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

  // TODO: 尝试执行请求
  async tryAcquire(): Promise<boolean> {
    // 实现步骤：
    const now = Date.now();

    // 【固定窗口策略】
    // if (this.strategy === 'fixed') {
    //   1. 检查窗口是否过期：
    //      if (now >= this.windowStart + this.windowMs) {
    //        this.windowStart = now
    //        this.requests = []  // 重置计数
    //      }
    //   2. 检查是否超限：
    //      if (this.requests.length < this.maxRequests) {
    //        this.requests.push(now)
    //        return true
    //      }
    //   3. 否则返回 false
    // }

    // 【滑动窗口策略】
    // else {
    //   1. 清理过期记录：
    //      this.requests = this.requests.filter(time => now - time < this.windowMs)
    //   2. 检查是否超限：
    //      if (this.requests.length < this.maxRequests) {
    //        this.requests.push(now)
    //        return true
    //      }
    //   3. 否则返回 false
    // }

    throw new Error('未实现');
  }

  // TODO: 执行带限流的函数
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    // 实现步骤：
    // 1. 无限循环等待获取权限：
    //    while (true) {
    //      const canProceed = await this.tryAcquire()
    //      if (canProceed) {
    //        return await fn()  // 获得权限，执行函数
    //      }
    //
    //      2. 计算需要等待的时间：
    //         - 滑动窗口：等待最早的请求过期
    //           if (this.strategy === 'sliding' && this.requests.length > 0) {
    //             const oldestRequest = this.requests[0]
    //             const waitTime = this.windowMs - (Date.now() - oldestRequest)
    //             if (waitTime > 0) {
    //               await new Promise(r => setTimeout(r, waitTime + 10))
    //             }
    //           }
    //         - 固定窗口：等待窗口重置
    //           else if (this.strategy === 'fixed') {
    //             const waitTime = this.windowStart + this.windowMs - Date.now()
    //             if (waitTime > 0) {
    //               await new Promise(r => setTimeout(r, waitTime + 10))
    //             }
    //           }
    //         - 否则短暂等待：
    //           else {
    //             await new Promise(r => setTimeout(r, 50))
    //           }
    //    }

    throw new Error('未实现');
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
