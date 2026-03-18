// 练习 17: 限制并发数量
//
// 当需要处理大量异步任务时，如果全部并发执行可能会耗尽资源
// 我们需要限制同时执行的任务数量

function fetchUrl(url: string): Promise<string> {
  return new Promise((resolve) => {
    const delay = Math.random() * 200 + 100;
    setTimeout(() => {
      resolve(`${url} 完成`);
    }, delay);
  });
}

// TODO: 实现一个函数，限制并发数量为 2
// 即同时最多只能有 2 个请求在执行
async function fetchWithLimit(urls: string[], limit: number): Promise<string[]> {
  const results: string[] = [];

  // 在这里实现代码
  // 提示：可以使用一个正在执行的任务队列
  // 当队列未满时，启动新任务
  // 当任务完成时，从队列中移除，并启动下一个任务

  return results;
}

// 测试代码
const urls = ['url1', 'url2', 'url3', 'url4', 'url5'];

fetchWithLimit(urls, 2).then((results) => {
  console.log('所有请求完成:');
  results.forEach((r) => console.log(`  ${r}`));

  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
