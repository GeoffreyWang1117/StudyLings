// 练习 28: 批量文件处理器
//
// 【学习目标】
// 在这个练习中，你将实现一个批量文件处理工具，学习：
// 1. 并发控制 - 限制同时处理的文件数量
// 2. 错误隔离 - 单个文件失败不影响其他文件
// 3. 重试机制 - 自动重试失败的操作
// 4. 进度报告 - 实时反馈处理进度
//
// 【核心概念】
// - 工作队列模式：维护待处理任务队列
// - 并发 worker：多个 worker 并发从队列取任务
// - 错误恢复：捕获错误，记录但不中断整体流程
// - 回调通知：使用回调函数报告进度
//
// 【实现提示】
// 1. processFile()：处理单个文件
//    - 使用 for 循环实现重试
//    - 读取 -> 转换 -> 写入
//    - 失败时等待后重试
//    - 返回成功或失败的结果
// 2. processBatch()：批量处理
//    - 创建队列（数组）存储待处理文件路径
//    - 创建多个 worker（根据 concurrency）
//    - 每个 worker 循环：从队列取任务 -> 处理 -> 报告进度
//    - 使用 Promise.all 等待所有 worker 完成
//    - 收集并分类结果
//
// 【预期行为】
// - 最多 concurrency 个文件同时处理
// - 单个文件失败会重试，但不影响其他文件
// - 实时显示处理进度
// - 最后统计成功和失败的文件

interface FileTask {
  path: string;
  content: string;
}

interface ProcessResult {
  path: string;
  success: boolean;
  result?: any;
  error?: string;
}

// 模拟文件读取
async function readFile(path: string): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (Math.random() < 0.1) {
        reject(new Error(`无法读取文件: ${path}`));
      } else {
        resolve(`Content of ${path}\nLine 1\nLine 2\nLine 3`);
      }
    }, Math.random() * 300 + 100);
  });
}

// 模拟文件写入
async function writeFile(path: string, content: string): Promise<void> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (Math.random() < 0.05) {
        reject(new Error(`无法写入文件: ${path}`));
      } else {
        resolve();
      }
    }, Math.random() * 200 + 100);
  });
}

// TODO: 实现批量文件处理器
class BatchFileProcessor {
  private concurrency: number;
  private retries: number;

  constructor(options: { concurrency?: number; retries?: number } = {}) {
    this.concurrency = options.concurrency || 3;
    this.retries = options.retries || 2;
  }

  // TODO: 处理单个文件
  async processFile(
    path: string,
    transformer: (content: string) => string
  ): Promise<ProcessResult> {
    // 实现步骤：
    // 1. 使用 for 循环实现重试（0 到 retries）
    // 2. 在 try 块中：
    //    - 读取文件：const content = await readFile(path)
    //    - 应用转换：const transformed = transformer(content)
    //    - 写入文件：await writeFile(path + '.processed', transformed)
    //    - 返回成功结果：{ path, success: true, result: outputPath }
    // 3. 在 catch 块中：
    //    - 记录错误：lastError = error
    //    - 如果不是最后一次重试，等待后继续循环
    //    - 等待时间：await new Promise(r => setTimeout(r, 100 * (attempt + 1)))
    // 4. 循环结束仍失败，返回失败结果：{ path, success: false, error: lastError.message }

    throw new Error('未实现');
  }

  // TODO: 批量处理文件
  async processBatch(
    paths: string[],
    transformer: (content: string) => string,
    onProgress?: (completed: number, total: number) => void
  ): Promise<{
    successful: ProcessResult[];
    failed: ProcessResult[];
  }> {
    // 实现步骤（工作队列模式）：
    // 1. 初始化：
    //    - const results: ProcessResult[] = []
    //    - const queue = [...paths]  // 复制数组作为队列
    //    - let completed = 0
    // 2. 定义 worker 函数：
    //    async function processNext() {
    //      while (queue.length > 0) {
    //        const path = queue.shift()  // 取出一个任务
    //        if (!path) break
    //        const result = await this.processFile(path, transformer)
    //        results.push(result)
    //        completed++
    //        if (onProgress) onProgress(completed, paths.length)
    //      }
    //    }
    // 3. 启动 workers：
    //    - 创建 concurrency 个 worker Promise
    //    - const workers = Array(this.concurrency).fill(0).map(() => processNext())
    // 4. 等待所有 worker 完成：await Promise.all(workers)
    // 5. 分类结果：
    //    - successful: results.filter(r => r.success)
    //    - failed: results.filter(r => !r.success)

    throw new Error('未实现');
  }
}

// 测试代码
async function testBatchFileProcessor() {
  const processor = new BatchFileProcessor({
    concurrency: 2,
    retries: 1,
  });

  // 转换函数：转换为大写
  const toUpperCase = (content: string) => content.toUpperCase();

  const files = [
    'file1.txt',
    'file2.txt',
    'file3.txt',
    'file4.txt',
    'file5.txt',
  ];

  console.log('开始批量处理文件...\n');

  const startTime = Date.now();

  const results = await processor.processBatch(
    files,
    toUpperCase,
    (completed, total) => {
      console.log(`进度: ${completed}/${total}`);
    }
  );

  const duration = Date.now() - startTime;

  console.log('\n' + '='.repeat(50));
  console.log('处理结果');
  console.log('='.repeat(50));
  console.log(`成功: ${results.successful.length}`);
  console.log(`失败: ${results.failed.length}`);
  console.log(`总耗时: ${duration}ms`);

  if (results.successful.length > 0) {
    console.log('\n成功的文件:');
    results.successful.forEach((r) => {
      console.log(`  ✓ ${r.path}`);
    });
  }

  if (results.failed.length > 0) {
    console.log('\n失败的文件:');
    results.failed.forEach((r) => {
      console.log(`  ✗ ${r.path}: ${r.error}`);
    });
  }

  console.log('\n✓ 测试完成');
}

testBatchFileProcessor();
