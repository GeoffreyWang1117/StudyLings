// 练习 17: 限制并发数量 - 答案

function fetchUrl(url: string): Promise<string> {
  return new Promise((resolve) => {
    const delay = Math.random() * 200 + 100;
    setTimeout(() => {
      resolve(`${url} 完成`);
    }, delay);
  });
}

async function fetchWithLimit(urls: string[], limit: number): Promise<string[]> {
  const results: string[] = [];
  const executing: Promise<void>[] = [];

  for (const url of urls) {
    const promise = fetchUrl(url).then((result) => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(
        executing.findIndex((p) => p === promise),
        1
      );
    }
  }

  await Promise.all(executing);
  return results;
}

const urls = ['url1', 'url2', 'url3', 'url4', 'url5'];

fetchWithLimit(urls, 2).then((results) => {
  console.log('所有请求完成:');
  results.forEach((r) => console.log(`  ${r}`));

  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
