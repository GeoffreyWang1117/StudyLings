// 练习 4: Promise 简介
//
// Promise 是异步编程的一个重要概念。一个 Promise 代表一个异步操作的最终完成或失败。
// Promise 有三种状态：
// - Pending (进行中)
// - Fulfilled (已成功)
// - Rejected (已失败)

// TODO: 创建一个 Promise，在 500ms 后 resolve 返回字符串 "Promise resolved!"
function createPromise(): Promise<string> {
  // 在这里实现代码
  return new Promise((resolve, reject) => {
    // 提示：使用 setTimeout 和 resolve
  });
}

// 测试代码
createPromise().then((result) => {
  console.log(result); // 应该输出: "Promise resolved!"

  // 验证
  if (result === 'Promise resolved!') {
    console.log('✓ 测试通过！');
    process.exit(0);
  } else {
    console.error('✗ 测试失败：返回值不正确');
    process.exit(1);
  }
});
