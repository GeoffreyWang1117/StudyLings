// 练习 14: 使用 try/catch 处理异步错误
//
// 在 async 函数中，可以使用 try/catch 来捕获异步操作的错误
// 这比 Promise 的 .catch() 更直观

function riskyOperation(): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const random = Math.random();
      if (random > 0.5) {
        resolve('操作成功！');
      } else {
        reject(new Error('操作失败！'));
      }
    }, 100);
  });
}

// TODO: 使用 try/catch 处理 riskyOperation() 可能的错误
async function handleRiskyOperation() {
  // 在这里实现代码
  // try {
  //   const result = await riskyOperation();
  //   console.log('成功:', result);
  // } catch (error) {
  //   console.log('错误:', error.message);
  // }
}

handleRiskyOperation().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
