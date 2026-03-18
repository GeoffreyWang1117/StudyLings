// 练习 22: Async Iterators（异步迭代器）
//
// 异步迭代器允许我们遍历异步数据源

// 模拟分页 API
async function fetchPage(page: number): Promise<number[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      // 返回该页的数据，最多 3 页
      if (page > 3) {
        resolve([]);
      } else {
        resolve([page * 10, page * 10 + 1, page * 10 + 2]);
      }
    }, 100);
  });
}

// TODO: 实现一个异步迭代器，逐页获取数据
async function* paginatedData(): AsyncIterableIterator<number[]> {
  // 在这里实现代码
  // 提示：使用 yield 返回每页的数据
  // 当没有更多数据时停止迭代
}

// 测试代码
(async () => {
  console.log('开始获取分页数据...');

  for await (const page of paginatedData()) {
    console.log('页面数据:', page);
  }

  console.log('✓ 所有数据获取完成');
  process.exit(0);
})();
