// 练习 20: 超时控制
//
// 有时我们需要为异步操作设置超时，避免无限等待

function slowOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('操作完成');
    }, 2000); // 2秒后完成
  });
}

function fastOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('快速完成');
    }, 500); // 0.5秒后完成
  });
}

// TODO: 实现一个 withTimeout 函数，为 Promise 添加超时控制
// 如果在超时时间内完成，返回结果；否则抛出超时错误
async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  // 在这里实现代码
  // 提示：使用 Promise.race()
  // 一个是原始 Promise，另一个是超时 Promise

  throw new Error('未实现');
}

// 测试代码
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
