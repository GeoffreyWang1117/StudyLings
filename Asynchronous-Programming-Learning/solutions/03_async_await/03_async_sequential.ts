// 练习 12: 顺序执行异步操作 - 答案

function task1(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('任务1完成'), 100);
  });
}

function task2(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('任务2完成'), 100);
  });
}

function task3(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('任务3完成'), 100);
  });
}

async function executeTasks() {
  const result1 = await task1();
  console.log(result1);

  const result2 = await task2();
  console.log(result2);

  const result3 = await task3();
  console.log(result3);
}

executeTasks().then(() => {
  setTimeout(() => {
    console.log('✓ 所有任务完成');
    process.exit(0);
  }, 500);
});
