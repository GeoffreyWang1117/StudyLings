// 练习 7: Promise 链式调用 - 答案

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

function executeSteps() {
  step1()
    .then((result1) => step2(result1))
    .then((result2) => step3(result2))
    .then((finalResult) => {
      console.log(`Final result: ${finalResult}`);
    });
}

executeSteps();

setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 500);
