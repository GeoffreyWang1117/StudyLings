// 练习 3: 回调地狱 - 答案

function step1(callback: (result: string) => void) {
  setTimeout(() => callback('Step 1 完成'), 100);
}

function step2(previousResult: string, callback: (result: string) => void) {
  setTimeout(() => callback(`${previousResult} -> Step 2 完成`), 100);
}

function step3(previousResult: string, callback: (result: string) => void) {
  setTimeout(() => callback(`${previousResult} -> Step 3 完成`), 100);
}

function executeSteps() {
  step1((result1) => {
    step2(result1, (result2) => {
      step3(result2, (result3) => {
        console.log(`Final result: ${result3}`);
      });
    });
  });
}

executeSteps();
