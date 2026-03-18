// 练习 12: 顺序执行异步操作
//
// 使用 await 可以让异步代码看起来像同步代码，更容易理解

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

// TODO: 使用 async/await 顺序执行三个任务
// 每完成一个任务就打印结果
async function executeTasks() {
  // 在这里实现代码
  // 提示：
  // const result1 = await task1();
  // console.log(result1);
  // ... 继续处理 task2 和 task3
}

executeTasks().then(() => {
  setTimeout(() => {
    console.log('✓ 所有任务完成');
    process.exit(0);
  }, 500);
});
