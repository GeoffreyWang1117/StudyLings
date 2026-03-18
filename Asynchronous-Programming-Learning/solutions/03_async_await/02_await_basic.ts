// 练习 11: await 基础用法 - 答案

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fetchData(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('数据已加载'), 100);
  });
}

async function loadData() {
  console.log('开始加载...');

  const data = await fetchData();
  console.log(data);

  console.log('加载完成！');
}

loadData().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
