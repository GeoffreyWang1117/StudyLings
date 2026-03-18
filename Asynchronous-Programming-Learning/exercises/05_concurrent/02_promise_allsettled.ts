// 练习 18: Promise.allSettled()
//
// Promise.all() 在任何一个 Promise 失败时就会立即失败
// Promise.allSettled() 会等待所有 Promise 完成（无论成功或失败）

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

// TODO: 使用 Promise.allSettled() 执行多个任务
// 包括成功和失败的任务，然后打印所有结果的状态
async function executeAllTasks() {
  const tasks = [
    task(1, false), // 成功
    task(2, true),  // 失败
    task(3, false), // 成功
    task(4, true),  // 失败
  ];

  // 在这里实现代码
  // 使用 Promise.allSettled(tasks)
  // 遍历结果，打印每个任务的状态和值/原因
}

executeAllTasks().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 300);
});
