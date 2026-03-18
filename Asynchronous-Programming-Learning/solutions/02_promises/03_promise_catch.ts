// 练习 6: 使用 .catch() 处理错误 - 答案

function fetchWithError(): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject(new Error('获取数据失败'));
    }, 100);
  });
}

async function handleError() {
  fetchWithError()
    .then((data) => {
      console.log('成功:', data);
    })
    .catch((error) => {
      console.log(`Error caught: ${error.message}`);
    });
}

handleError().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
