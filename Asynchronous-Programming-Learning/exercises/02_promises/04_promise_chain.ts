// 练习 7: Promise 链式调用
//
// Promise 可以链式调用，每个 .then() 都会返回一个新的 Promise
// 这样可以避免回调地狱，让代码更清晰

function step1(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('Step 1'), 100);
  });
}

function step2(prev: string): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(`${prev} -> Step 2`), 100);
  });
}

function step3(prev: string): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(`${prev} -> Step 3`), 100);
  });
}

// TODO: 使用 Promise 链式调用完成三个步骤，最后打印最终结果
// 对比练习 3 的回调地狱，是不是清晰多了？
function executeSteps() {
  // 在这里实现代码
  // 格式：step1().then(...).then(...).then(...)
}

executeSteps();

// 验证：应该输出 "Final result: Step 1 -> Step 2 -> Step 3"
setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 500);
