// 练习 19: 重试机制 - 答案

let attemptCount = 0;

function unreliableOperation(): Promise<string> {
  attemptCount++;
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (attemptCount < 3) {
        reject(new Error(`尝试 ${attemptCount} 失败`));
      } else {
        resolve('操作成功！');
      }
    }, 100);
  });
}

async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number,
  delay: number = 100
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const result = await fn();
      return result;
    } catch (error: any) {
      lastError = error;
      console.log(`尝试 ${i + 1}/${maxRetries} 失败: ${error.message}`);

      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
}

retry(() => unreliableOperation(), 3, 100)
  .then((result) => {
    console.log(`最终结果: ${result}`);
    console.log(`总尝试次数: ${attemptCount}`);

    setTimeout(() => {
      console.log('✓ 测试完成');
      process.exit(0);
    }, 200);
  })
  .catch((error) => {
    console.error('重试失败:', error.message);
    process.exit(1);
  });
