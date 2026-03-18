// 练习 26: HTTP 客户端封装
//
// 【学习目标】
// 在这个练习中，你将创建一个功能完整的 HTTP 客户端，综合应用：
// 1. 请求缓存机制 - 避免重复请求，提升性能
// 2. 自动重试逻辑 - 处理网络不稳定情况
// 3. 超时控制 - 避免请求长时间挂起
// 4. 错误处理 - 优雅地处理各种异常情况
//
// 【核心概念】
// - Promise 超时控制：使用 Promise.race 实现超时
// - 指数退避重试：每次重试增加等待时间
// - LRU 缓存：记录请求结果，GET 请求可以从缓存读取
// - 时间戳验证：缓存过期机制
//
// 【实现提示】
// 1. 构造函数：初始化默认配置（超时、重试次数、缓存时长）
// 2. request 方法：核心请求逻辑
//    - 检查是否有缓存（仅 GET 请求）
//    - 实现超时控制（Promise.race）
//    - 失败时自动重试，每次重试增加等待时间
//    - 成功后缓存结果
// 3. get/post 方法：便捷方法，调用 request
// 4. clearCache：清空缓存
//
// 【预期行为】
// - 首次 GET 请求会真正发起网络请求
// - 再次请求同一 URL，会从缓存返回（速度明显更快）
// - POST 请求不使用缓存
// - 网络失败时自动重试
// - 超时会抛出错误

interface RequestConfig {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  timeout?: number;
  retries?: number;
}

interface Response {
  status: number;
  data: any;
  headers: Record<string, string>;
}

// 模拟 HTTP 请求
async function mockFetch(url: string, options: any = {}): Promise<Response> {
  return new Promise((resolve, reject) => {
    const delay = Math.random() * 500 + 100;

    setTimeout(() => {
      // 10% 失败率
      if (Math.random() < 0.1) {
        reject(new Error('Network error'));
      } else {
        resolve({
          status: 200,
          data: { message: `Response from ${url}`, timestamp: Date.now() },
          headers: { 'content-type': 'application/json' },
        });
      }
    }, delay);
  });
}

// TODO: 实现 HttpClient 类
class HttpClient {
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private defaultTimeout: number = 5000;
  private defaultRetries: number = 3;
  private cacheTimeout: number = 60000; // 1分钟

  constructor(config?: { timeout?: number; retries?: number; cacheTimeout?: number }) {
    // TODO: 在这里实现构造函数
    // 提示：使用 config 参数更新默认值
  }

  // TODO: 实现请求方法
  async request(config: RequestConfig): Promise<Response> {
    // 要求：
    // 1. 检查缓存（GET 请求）
    //    - 如果是 GET 且缓存存在且未过期，直接返回缓存
    //    - 缓存 key 使用 URL
    // 2. 添加超时控制
    //    - 使用 Promise.race([请求, 超时 Promise])
    //    - 超时 Promise: new Promise((_, reject) => setTimeout(() => reject(...), timeout))
    // 3. 实现重试机制
    //    - 使用 for 循环，从 0 到 retries
    //    - 失败后等待：await new Promise(r => setTimeout(r, 延迟时间))
    //    - 延迟时间可以是固定的，或使用指数退避（100ms * 2^attempt）
    // 4. 缓存成功的响应
    //    - 仅缓存 GET 请求的成功响应
    //    - 缓存格式：{ data: response, timestamp: Date.now() }

    throw new Error('未实现');
  }

  // TODO: 实现便捷方法
  async get(url: string, config?: Partial<RequestConfig>): Promise<Response> {
    // 提示：调用 request 方法，合并配置
    // return this.request({ url, method: 'GET', ...config })
    throw new Error('未实现');
  }

  async post(url: string, body: any, config?: Partial<RequestConfig>): Promise<Response> {
    // 提示：调用 request 方法，传入 body
    // return this.request({ url, method: 'POST', body, ...config })
    throw new Error('未实现');
  }

  // TODO: 清除缓存
  clearCache(): void {
    // 提示：this.cache.clear()
  }
}

// 测试代码
async function testHttpClient() {
  const client = new HttpClient({
    timeout: 3000,
    retries: 2,
    cacheTimeout: 30000,
  });

  console.log('测试 1: 普通 GET 请求');
  try {
    const response1 = await client.get('https://api.example.com/users');
    console.log('✓ 请求成功:', response1.data);
  } catch (error: any) {
    console.error('✗ 请求失败:', error.message);
  }

  console.log('\n测试 2: 缓存测试');
  const start = Date.now();
  await client.get('https://api.example.com/posts/1');
  const firstRequestTime = Date.now() - start;

  const start2 = Date.now();
  await client.get('https://api.example.com/posts/1'); // 应该从缓存读取
  const secondRequestTime = Date.now() - start2;

  console.log(`首次请求: ${firstRequestTime}ms`);
  console.log(`缓存请求: ${secondRequestTime}ms`);
  console.log(secondRequestTime < firstRequestTime / 2 ? '✓ 缓存工作正常' : '✗ 缓存未生效');

  console.log('\n测试 3: POST 请求（不缓存）');
  try {
    const response3 = await client.post('https://api.example.com/users', {
      name: 'John Doe',
    });
    console.log('✓ POST 成功:', response3.data);
  } catch (error: any) {
    console.error('✗ POST 失败:', error.message);
  }

  console.log('\n✓ 所有测试完成');
}

testHttpClient();
