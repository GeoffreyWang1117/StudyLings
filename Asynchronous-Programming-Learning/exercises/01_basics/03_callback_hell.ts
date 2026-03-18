// 练习 3: 回调地狱 (Callback Hell)
//
// 当我们需要进行多个连续的异步操作时，使用回调函数会导致代码层层嵌套，
// 这种情况被称为"回调地狱"或"末日金字塔"。

// 模拟异步操作
function step1(callback: (result: string) => void) {
  setTimeout(() => callback('Step 1 完成'), 100);
}

function step2(previousResult: string, callback: (result: string) => void) {
  setTimeout(() => callback(`${previousResult} -> Step 2 完成`), 100);
}

function step3(previousResult: string, callback: (result: string) => void) {
  setTimeout(() => callback(`${previousResult} -> Step 3 完成`), 100);
}

// TODO: 使用回调函数完成三个步骤的调用，最后打印最终结果
// 体会一下回调地狱的感觉
function executeSteps() {
  // 在这里实现代码
  // 应该是嵌套的回调结构
}

executeSteps();

// 验证：应该输出 "Step 1 完成 -> Step 2 完成 -> Step 3 完成"
//
// 思考：这种嵌套的代码可读性如何？如果有更多步骤会怎样？
// 这就是为什么我们需要 Promise 和 async/await！
