// 练习 27: 数据库连接池 - 答案

interface DbConnection {
  id: number;
  query(sql: string): Promise<any>;
  close(): void;
}

class MockConnection implements DbConnection {
  constructor(public id: number) {}

  async query(sql: string): Promise<any> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          rows: [{ id: 1, name: 'Test Data' }],
          sql,
          connection: this.id,
        });
      }, Math.random() * 200 + 100);
    });
  }

  close(): void {
    console.log(`  连接 ${this.id} 已关闭`);
  }
}

class ConnectionPool {
  private connections: DbConnection[] = [];
  private available: DbConnection[] = [];
  private waiting: Array<(conn: DbConnection) => void> = [];
  private maxConnections: number;
  private currentId: number = 0;

  constructor(maxConnections: number = 5) {
    this.maxConnections = maxConnections;
  }

  async acquire(): Promise<DbConnection> {
    // 如果有可用连接，直接返回
    if (this.available.length > 0) {
      const conn = this.available.pop()!;
      return conn;
    }

    // 如果未达到最大连接数，创建新连接
    if (this.connections.length < this.maxConnections) {
      const conn = new MockConnection(++this.currentId);
      this.connections.push(conn);
      return conn;
    }

    // 否则等待其他查询释放连接
    return new Promise((resolve) => {
      this.waiting.push(resolve);
    });
  }

  release(connection: DbConnection): void {
    // 如果有等待的请求，分配给它
    if (this.waiting.length > 0) {
      const resolve = this.waiting.shift()!;
      resolve(connection);
    } else {
      // 否则放回可用池
      this.available.push(connection);
    }
  }

  async query(sql: string): Promise<any> {
    const connection = await this.acquire();
    try {
      return await connection.query(sql);
    } finally {
      this.release(connection);
    }
  }

  async closeAll(): Promise<void> {
    this.connections.forEach((conn) => conn.close());
    this.connections = [];
    this.available = [];
    this.waiting = [];
  }

  getStatus() {
    return {
      total: this.connections.length,
      available: this.available.length,
      inUse: this.connections.length - this.available.length,
      waiting: this.waiting.length,
    };
  }
}

async function testConnectionPool() {
  const pool = new ConnectionPool(3);

  console.log('测试 1: 并发查询（超过池大小）');
  const queries = [];

  for (let i = 1; i <= 5; i++) {
    queries.push(
      (async () => {
        console.log(`查询 ${i} 开始`);
        const result = await pool.query(`SELECT * FROM users WHERE id = ${i}`);
        console.log(`查询 ${i} 完成，使用连接 ${result.connection}`);
        return result;
      })()
    );
  }

  await Promise.all(queries);

  console.log('\n测试 2: 池状态');
  const status = pool.getStatus();
  console.log(`总连接数: ${status.total}`);
  console.log(`可用连接: ${status.available}`);
  console.log(`使用中: ${status.inUse}`);
  console.log(`等待中: ${status.waiting}`);

  console.log('\n测试 3: 顺序查询');
  await pool.query('SELECT * FROM posts');
  await pool.query('SELECT * FROM comments');

  console.log('\n清理连接池...');
  await pool.closeAll();

  console.log('\n✓ 所有测试完成');
}

testConnectionPool();
