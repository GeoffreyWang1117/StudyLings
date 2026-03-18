// 练习 16: finally 块 - 答案

function fetchData(shouldFail: boolean): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error('获取数据失败'));
      } else {
        resolve('数据获取成功');
      }
    }, 100);
  });
}

async function fetchWithCleanup(shouldFail: boolean) {
  console.log('开始获取数据...');

  try {
    const data = await fetchData(shouldFail);
    console.log('成功:', data);
  } catch (error: any) {
    console.log('错误:', error.message);
  } finally {
    console.log('清理资源完成');
  }
}

(async () => {
  await fetchWithCleanup(false);
  console.log('---');
  await fetchWithCleanup(true);

  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 500);
})();
