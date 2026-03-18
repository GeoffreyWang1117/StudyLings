// 练习 5: 使用 .then() 处理 Promise - 答案

function fetchNumber(): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(42), 100);
  });
}

async function processNumber() {
  fetchNumber().then((number) => {
    const result = number * 2;
    console.log(`Result: ${result}`);
  });
}

processNumber().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
