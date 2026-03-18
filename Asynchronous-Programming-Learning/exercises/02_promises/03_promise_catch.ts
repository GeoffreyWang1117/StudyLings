// 练习 6: 使用 .catch() 处理错误
//
// .catch() 方法用于处理 Promise 失败（reject）时的情况

function fetchWithError(): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject(new Error('获取数据失败'));
    }, 100);
  });
}

// TODO: 使用 .catch() 捕获错误，并打印 "Error caught: <错误信息>"
async function handleError() {
  // 在这里实现代码
  // 提示：使用 fetchWithError().catch(...)
}

// 测试代码
handleError().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
