// 练习 4: Promise 简介 - 答案

function createPromise(): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('Promise resolved!');
    }, 500);
  });
}

createPromise().then((result) => {
  console.log(result);

  if (result === 'Promise resolved!') {
    console.log('✓ 测试通过！');
    process.exit(0);
  } else {
    console.error('✗ 测试失败：返回值不正确');
    process.exit(1);
  }
});
