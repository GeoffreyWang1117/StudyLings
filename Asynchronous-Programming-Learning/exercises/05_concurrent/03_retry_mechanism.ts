// 练习 19: 重试机制
//
// 在网络请求等场景中，失败可能是暂时的
// 实现一个重试机制可以提高成功率

let attemptCount = 0;

function unreliableOperation(): Promise<string> {
  attemptCount++;
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // 前两次尝试失败，第三次成功
      if (attemptCount < 3) {
        reject(new Error(`尝试 ${attemptCount} 失败`));
      } else {
        resolve('操作成功！');
      }
    }, 100);
  });
}

// TODO: 实现一个重试函数，最多重试 maxRetries 次
async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number,
  delay: number = 100
): Promise<T> {
  // 在这里实现代码
  // 提示：使用循环或递归
  // 捕获错误，如果还有重试次数则继续尝试
  // 可以在重试之间添加延迟

  throw new Error('未实现');
}

// 测试代码
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
