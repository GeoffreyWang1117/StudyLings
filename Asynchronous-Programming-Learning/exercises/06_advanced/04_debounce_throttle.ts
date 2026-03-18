// 练习 24: 防抖（Debounce）和节流（Throttle）
//
// 这两种技术常用于优化频繁触发的异步操作

// TODO: 实现一个防抖函数
// 防抖：在事件触发 n 秒后才执行，如果 n 秒内又触发，则重新计时
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  // 在这里实现代码
  // 提示：使用 setTimeout 和闭包
}

// TODO: 实现一个节流函数
// 节流：在 n 秒内只执行一次，如果 n 秒内多次触发，只执行第一次
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  // 在这里实现代码
  // 提示：使用时间戳判断
}

// 测试代码
console.log('测试防抖:');
let debounceCount = 0;
const debouncedFn = debounce(() => {
  debounceCount++;
  console.log(`防抖函数执行 (${debounceCount})`);
}, 100);

// 快速调用 5 次
for (let i = 0; i < 5; i++) {
  debouncedFn();
}
// 应该只执行一次

setTimeout(() => {
  console.log('\n测试节流:');
  let throttleCount = 0;
  const throttledFn = throttle(() => {
    throttleCount++;
    console.log(`节流函数执行 (${throttleCount})`);
  }, 100);

  // 快速调用 5 次
  for (let i = 0; i < 5; i++) {
    throttledFn();
  }
  // 应该立即执行一次，然后被节流

  setTimeout(() => {
    console.log('\n✓ 测试完成');
    process.exit(0);
  }, 500);
}, 500);
