// 练习 11: await 基础用法
//
// await 关键字只能在 async 函数内使用
// await 会暂停函数执行，直到 Promise 完成，然后返回结果

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fetchData(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('数据已加载'), 100);
  });
}

// TODO: 使用 await 等待 fetchData() 完成，然后打印结果
async function loadData() {
  console.log('开始加载...');

  // 在这里使用 await
  // 提示：const data = await fetchData();

  console.log('加载完成！');
}

loadData().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 200);
});
