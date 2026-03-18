// 练习 21: Event Loop 理解
//
// Event Loop 是 JavaScript 异步编程的核心机制
// 理解执行顺序对于写好异步代码至关重要

console.log('1');

setTimeout(() => {
  console.log('2');
}, 0);

Promise.resolve().then(() => {
  console.log('3');
});

console.log('4');

// TODO: 在运行代码之前，预测输出顺序
// 然后运行代码验证你的理解
//
// 问题：
// 1. 为什么 setTimeout 设置为 0ms，但不是第二个执行？
// 2. Promise.then() 为什么比 setTimeout 先执行？
// 3. 什么是微任务（microtask）和宏任务（macrotask）？
//
// 预期输出顺序：
// 1
// 4
// 3
// 2
//
// 解释：
// - 同步代码（1, 4）首先执行
// - Promise.then() 是微任务，优先于宏任务
// - setTimeout 是宏任务，最后执行
