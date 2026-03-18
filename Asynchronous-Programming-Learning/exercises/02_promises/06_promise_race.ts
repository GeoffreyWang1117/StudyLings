// 练习 9: Promise.race() 竞速
//
// Promise.race() 返回最先完成（无论成功或失败）的 Promise 的结果

function fastOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('快速操作完成'), 100);
  });
}

function slowOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('慢速操作完成'), 500);
  });
}

// TODO: 使用 Promise.race() 获取最先完成的操作结果
// 打印 "Winner: <结果>"
async function raceOperations() {
  // 在这里实现代码
  // 提示：Promise.race([fastOperation(), slowOperation()])
}

raceOperations();

// 验证：应该输出 "Winner: 快速操作完成"
setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 300);
