// 练习 15: 错误传播 - 答案

function step1(): Promise<string> {
  return Promise.resolve('Step 1 成功');
}

function step2(): Promise<string> {
  return Promise.reject(new Error('Step 2 失败'));
}

function step3(): Promise<string> {
  return Promise.resolve('Step 3 成功');
}

async function executeWithErrorHandling() {
  try {
    const result1 = await step1();
    console.log(result1);

    const result2 = await step2();
    console.log(result2);

    const result3 = await step3();
    console.log(result3);
  } catch (error: any) {
    console.log('捕获到错误:', error.message);
  }
}

executeWithErrorHandling().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
