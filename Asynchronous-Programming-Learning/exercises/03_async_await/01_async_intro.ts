// 练习 10: async 函数简介
//
// async 关键字用于声明一个异步函数
// async 函数总是返回一个 Promise

// TODO: 创建一个 async 函数，返回字符串 "Hello from async"
async function greet(): Promise<string> {
  // 在这里实现代码
  // 提示：在 async 函数中，return 的值会被自动包装成 Promise
  return '';
}

// 测试代码
greet().then((message) => {
  console.log(message);

  if (message === 'Hello from async') {
    console.log('✓ 测试通过！');
    process.exit(0);
  } else {
    console.error('✗ 测试失败');
    process.exit(1);
  }
});
