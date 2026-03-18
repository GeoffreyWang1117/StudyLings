// 练习 14: 使用 try/catch 处理异步错误 - 答案

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

async function handleRiskyOperation() {
  try {
    const result = await riskyOperation();
    console.log('成功:', result);
  } catch (error: any) {
    console.log('错误:', error.message);
  }
}

handleRiskyOperation().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
