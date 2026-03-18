// 练习 15: 错误传播
//
// 在 Promise 链或 async 函数中，错误会向上传播
// 直到被 catch 捕获

function step1(): Promise<string> {
  return Promise.resolve('Step 1 成功');
}

function step2(): Promise<string> {
  return Promise.reject(new Error('Step 2 失败'));
}

function step3(): Promise<string> {
  return Promise.resolve('Step 3 成功');
}

// TODO: 执行三个步骤，捕获并处理可能的错误
// 打印每个成功的步骤，如果有错误则打印错误信息
async function executeWithErrorHandling() {
  // 在这里实现代码
  // 提示：可以为每个步骤单独 try/catch，
  // 或者用一个大的 try/catch 包裹所有步骤
}

executeWithErrorHandling().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
