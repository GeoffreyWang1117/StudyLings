// 练习 22: Async Iterators - 答案

async function fetchPage(page: number): Promise<number[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (page > 3) {
        resolve([]);
      } else {
        resolve([page * 10, page * 10 + 1, page * 10 + 2]);
      }
    }, 100);
  });
}

async function* paginatedData(): AsyncIterableIterator<number[]> {
  let page = 1;

  while (true) {
    const data = await fetchPage(page);

    if (data.length === 0) {
      break;
    }

    yield data;
    page++;
  }
}

(async () => {
  console.log('开始获取分页数据...');

  for await (const page of paginatedData()) {
    console.log('页面数据:', page);
  }

  console.log('✓ 所有数据获取完成');
  process.exit(0);
})();
