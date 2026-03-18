// 练习 26: HTTP 客户端封装 - 答案

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

async function mockFetch(url: string, options: any = {}): Promise<Response> {
  return new Promise((resolve, reject) => {
    const delay = Math.random() * 500 + 100;

    setTimeout(() => {
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

class HttpClient {
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private defaultTimeout: number = 5000;
  private defaultRetries: number = 3;
  private cacheTimeout: number = 60000;

  constructor(config?: { timeout?: number; retries?: number; cacheTimeout?: number }) {
    if (config?.timeout) this.defaultTimeout = config.timeout;
    if (config?.retries) this.defaultRetries = config.retries;
    if (config?.cacheTimeout) this.cacheTimeout = config.cacheTimeout;
  }

  async request(config: RequestConfig): Promise<Response> {
    const method = config.method || 'GET';
    const timeout = config.timeout || this.defaultTimeout;
    const retries = config.retries ?? this.defaultRetries;

    // 检查缓存（仅 GET 请求）
    if (method === 'GET') {
      const cached = this.cache.get(config.url);
      if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
        return {
          status: 200,
          data: cached.data,
          headers: { 'x-cache': 'HIT' },
        };
      }
    }

    // 带超时和重试的请求
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const timeoutPromise = new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error('Request timeout')), timeout)
        );

        const response = await Promise.race([
          mockFetch(config.url, { method, body: config.body }),
          timeoutPromise,
        ]);

        // 缓存成功的 GET 响应
        if (method === 'GET') {
          this.cache.set(config.url, {
            data: response.data,
            timestamp: Date.now(),
          });
        }

        return response;
      } catch (error: any) {
        if (attempt < retries) {
          console.log(`  重试 ${attempt + 1}/${retries}...`);
          await new Promise((r) => setTimeout(r, 100 * (attempt + 1)));
        } else {
          throw error;
        }
      }
    }

    throw new Error('Max retries reached');
  }

  async get(url: string, config?: Partial<RequestConfig>): Promise<Response> {
    return this.request({ ...config, url, method: 'GET' });
  }

  async post(url: string, body: any, config?: Partial<RequestConfig>): Promise<Response> {
    return this.request({ ...config, url, method: 'POST', body });
  }

  clearCache(): void {
    this.cache.clear();
  }
}

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
  await client.get('https://api.example.com/posts/1');
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
