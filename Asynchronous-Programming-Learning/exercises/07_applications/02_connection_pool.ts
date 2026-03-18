// 练习 27: 数据库连接池
//
// 【学习目标】
// 在这个练习中，你将实现一个数据库连接池，学习：
// 1. 资源池模式 - 管理有限的昂贵资源
// 2. 等待队列 - 当资源不足时排队等待
// 3. 自动资源分配 - 先到先得的公平分配
// 4. 资源生命周期管理 - 创建、使用、释放、关闭
//
// 【核心概念】
// - 连接池：复用数据库连接，避免频繁创建销毁
// - 信号量模式：控制对有限资源的并发访问
// - Promise 等待队列：使用 Promise 实现阻塞等待
// - try/finally 模式：确保资源一定被释放
//
// 【实现提示】
// 1. acquire()：获取连接
//    - 如果有可用连接，立即返回
//    - 如果未达到最大连接数，创建新连接
//    - 否则，返回一个 Promise，加入等待队列
// 2. release()：释放连接
//    - 如果有等待的请求，分配给它（调用队列中的 resolve）
//    - 否则，放回 available 数组
// 3. query()：执行查询
//    - 获取连接，执行查询，释放连接
//    - 使用 try/finally 确保连接被释放
// 4. closeAll()：关闭所有连接
//
// 【预期行为】
// - 并发查询数不超过最大连接数
// - 超过限制的查询会等待
// - 连接会被复用
// - 所有查询都能完成

interface DbConnection {
  id: number;
  query(sql: string): Promise<any>;
  close(): void;
}

// 模拟数据库连接
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

// TODO: 实现连接池
class ConnectionPool {
  private connections: DbConnection[] = [];
  private available: DbConnection[] = [];
  private waiting: Array<(conn: DbConnection) => void> = [];
  private maxConnections: number;
  private currentId: number = 0;

  constructor(maxConnections: number = 5) {
    this.maxConnections = maxConnections;
    // TODO: 在这里实现初始化（可选，已在属性初始化）
  }

  // TODO: 获取连接
  async acquire(): Promise<DbConnection> {
    // 实现步骤：
    // 1. 如果有可用连接（available.length > 0）
    //    - 从 available 数组取出一个连接并返回
    // 2. 如果没有达到最大连接数（connections.length < maxConnections）
    //    - 创建新连接：new MockConnection(++this.currentId)
    //    - 添加到 connections 数组
    //    - 返回新连接
    // 3. 否则（需要等待）
    //    - 返回一个 Promise，将 resolve 函数保存到 waiting 数组
    //    - 当其他连接释放时，会调用这个 resolve
    //    提示：return new Promise<DbConnection>(resolve => this.waiting.push(resolve))

    throw new Error('未实现');
  }

  // TODO: 释放连接
  release(connection: DbConnection): void {
    // 实现步骤：
    // 1. 如果有等待的请求（waiting.length > 0）
    //    - 从 waiting 数组取出第一个 resolve 函数
    //    - 调用它，传入 connection：resolve(connection)
    // 2. 否则
    //    - 将连接放回 available 数组：this.available.push(connection)

    throw new Error('未实现');
  }

  // TODO: 执行查询（自动获取和释放连接）
  async query(sql: string): Promise<any> {
    // 实现步骤：
    // 1. 获取连接：const conn = await this.acquire()
    // 2. 使用 try/finally 模式：
    //    try {
    //      return await conn.query(sql)
    //    } finally {
    //      this.release(conn)  // 确保连接被释放
    //    }

    throw new Error('未实现');
  }

  // TODO: 关闭所有连接
  async closeAll(): Promise<void> {
    // 实现步骤：
    // 1. 遍历所有连接：this.connections.forEach(conn => conn.close())
    // 2. 清空数组：this.connections = []、this.available = []
  }

  // 获取池状态
  getStatus() {
    return {
      total: this.connections.length,
      available: this.available.length,
      inUse: this.connections.length - this.available.length,
      waiting: this.waiting.length,
    };
  }
}

// 测试代码
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
