// 练习 28: 批量文件处理器 - 答案
//
// 实现一个批量处理文件的工具，应用并发控制和错误处理

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

// 实现批量文件处理器
class BatchFileProcessor {
  private concurrency: number;
  private retries: number;

  constructor(options: { concurrency?: number; retries?: number } = {}) {
    this.concurrency = options.concurrency || 3;
    this.retries = options.retries || 2;
  }

  // 处理单个文件
  async processFile(
    path: string,
    transformer: (content: string) => string
  ): Promise<ProcessResult> {
    let lastError: Error | null = null;

    // 实现重试机制
    for (let attempt = 0; attempt <= this.retries; attempt++) {
      try {
        // 1. 读取文件
        const content = await readFile(path);

        // 2. 应用转换函数
        const transformed = transformer(content);

        // 3. 写入新文件（添加 .processed 后缀）
        const outputPath = `${path}.processed`;
        await writeFile(outputPath, transformed);

        // 4. 返回成功结果
        return {
          path,
          success: true,
          result: outputPath,
        };
      } catch (error) {
        lastError = error as Error;
        // 如果不是最后一次尝试，等待一会儿再重试
        if (attempt < this.retries) {
          await new Promise((resolve) => setTimeout(resolve, 100 * (attempt + 1)));
        }
      }
    }

    // 所有重试都失败了
    return {
      path,
      success: false,
      error: lastError?.message || '未知错误',
    };
  }

  // 批量处理文件
  async processBatch(
    paths: string[],
    transformer: (content: string) => string,
    onProgress?: (completed: number, total: number) => void
  ): Promise<{
    successful: ProcessResult[];
    failed: ProcessResult[];
  }> {
    const results: ProcessResult[] = [];
    const queue = [...paths];
    const inProgress: Promise<void>[] = [];
    let completed = 0;

    // 限制并发数的处理函数
    const processNext = async (): Promise<void> => {
      while (queue.length > 0) {
        const path = queue.shift();
        if (!path) break;

        const result = await this.processFile(path, transformer);
        results.push(result);
        completed++;

        // 报告进度
        if (onProgress) {
          onProgress(completed, paths.length);
        }
      }
    };

    // 启动并发worker
    for (let i = 0; i < Math.min(this.concurrency, paths.length); i++) {
      inProgress.push(processNext());
    }

    // 等待所有任务完成
    await Promise.all(inProgress);

    // 分类结果
    const successful = results.filter((r) => r.success);
    const failed = results.filter((r) => !r.success);

    return { successful, failed };
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
