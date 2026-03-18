// 练习 5: 使用 .then() 处理 Promise
//
// .then() 方法用于处理 Promise 成功时的结果

function fetchNumber(): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(42), 100);
  });
}

// TODO: 使用 .then() 获取 fetchNumber() 的结果，
// 将结果乘以 2，然后打印 "Result: <结果>"
async function processNumber() {
  // 在这里实现代码
  // 提示：使用 fetchNumber().then(...)
}

// 测试代码
processNumber().then(() => {
  // 验证会在异步操作后执行
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
