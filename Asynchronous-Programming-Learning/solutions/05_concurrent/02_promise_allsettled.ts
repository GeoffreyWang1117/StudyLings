// 练习 18: Promise.allSettled() - 答案

function task(id: number, shouldFail: boolean): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error(`任务 ${id} 失败`));
      } else {
        resolve(`任务 ${id} 成功`);
      }
    }, 100);
  });
}

async function executeAllTasks() {
  const tasks = [
    task(1, false),
    task(2, true),
    task(3, false),
    task(4, true),
  ];

  const results = await Promise.allSettled(tasks);

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      console.log(`任务 ${index + 1}: 成功 - ${result.value}`);
    } else {
      console.log(`任务 ${index + 1}: 失败 - ${result.reason.message}`);
    }
  });
}

executeAllTasks().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 300);
});
