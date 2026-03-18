// 练习 16: finally 块
//
// finally 块中的代码总是会执行，无论操作成功还是失败
// 常用于清理资源（关闭文件、断开连接等）

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

// TODO: 使用 try/catch/finally 处理数据获取
// finally 块中打印 "清理资源完成"
async function fetchWithCleanup(shouldFail: boolean) {
  console.log('开始获取数据...');

  // 在这里实现代码
  // try {
  //   ...
  // } catch (error) {
  //   ...
  // } finally {
  //   console.log('清理资源完成');
  // }
}

// 测试成功和失败两种情况
(async () => {
  await fetchWithCleanup(false);
  console.log('---');
  await fetchWithCleanup(true);

  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 500);
})();
