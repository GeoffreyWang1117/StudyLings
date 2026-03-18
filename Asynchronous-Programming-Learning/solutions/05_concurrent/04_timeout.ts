// 练习 20: 超时控制 - 答案

function slowOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('操作完成');
    }, 2000);
  });
}

function fastOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('快速完成');
    }, 500);
  });
}

async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(new Error(`操作超时（${timeoutMs}ms）`));
    }, timeoutMs);
  });

  return Promise.race([promise, timeoutPromise]);
}

(async () => {
  // 测试 1: 快速操作应该成功
  try {
    const result1 = await withTimeout(fastOperation(), 1000);
    console.log(`测试1: ${result1}`);
  } catch (error: any) {
    console.error(`测试1 失败: ${error.message}`);
  }

  // 测试 2: 慢速操作应该超时
  try {
    const result2 = await withTimeout(slowOperation(), 1000);
    console.log(`测试2: ${result2}`);
  } catch (error: any) {
    console.log(`测试2: ${error.message} (这是预期的)`);
  }

  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 500);
})();
