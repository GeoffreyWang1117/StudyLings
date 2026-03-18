// 练习 13: 并行执行异步操作 - 答案

function downloadFile(filename: string, size: number): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`${filename} (${size}MB) 下载完成`);
    }, size * 50);
  });
}

async function downloadFiles() {
  console.log('开始并行下载...');
  const startTime = Date.now();

  const results = await Promise.all([
    downloadFile('file1.txt', 2),
    downloadFile('file2.txt', 3),
    downloadFile('file3.txt', 1),
  ]);

  results.forEach((result) => console.log(result));

  const endTime = Date.now();
  console.log(`总耗时: ${endTime - startTime}ms`);
}

downloadFiles().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 500);
});
