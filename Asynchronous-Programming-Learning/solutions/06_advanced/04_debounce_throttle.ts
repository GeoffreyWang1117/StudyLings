// 练习 24: 防抖和节流 - 答案

function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout | null = null;

  return function (...args: Parameters<T>) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}

function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastCall = 0;

  return function (...args: Parameters<T>) {
    const now = Date.now();

    if (now - lastCall >= delay) {
      lastCall = now;
      fn(...args);
    }
  };
}

// 测试代码
console.log('测试防抖:');
let debounceCount = 0;
const debouncedFn = debounce(() => {
  debounceCount++;
  console.log(`防抖函数执行 (${debounceCount})`);
}, 100);

for (let i = 0; i < 5; i++) {
  debouncedFn();
}

setTimeout(() => {
  console.log('\n测试节流:');
  let throttleCount = 0;
  const throttledFn = throttle(() => {
    throttleCount++;
    console.log(`节流函数执行 (${throttleCount})`);
  }, 100);

  for (let i = 0; i < 5; i++) {
    throttledFn();
  }

  setTimeout(() => {
    console.log('\n✓ 测试完成');
    process.exit(0);
  }, 500);
}, 500);
