// 练习 10: async 函数简介 - 答案

async function greet(): Promise<string> {
  return 'Hello from async';
}

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
