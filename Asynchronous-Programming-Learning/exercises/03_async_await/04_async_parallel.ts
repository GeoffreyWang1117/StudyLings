// 练习 13: 并行执行异步操作
//
// 虽然 await 是顺序执行，但配合 Promise.all() 可以实现并行执行

function downloadFile(filename: string, size: number): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`${filename} (${size}MB) 下载完成`);
    }, size * 50); // 模拟下载时间与文件大小成正比
  });
}

// TODO: 并行下载三个文件，然后打印所有结果
// 文件: file1.txt (2MB), file2.txt (3MB), file3.txt (1MB)
async function downloadFiles() {
  console.log('开始并行下载...');
  const startTime = Date.now();

  // 在这里实现代码
  // 提示：使用 Promise.all() 和 await
  // const results = await Promise.all([...]);

  const endTime = Date.now();
  console.log(`总耗时: ${endTime - startTime}ms`);

  // 注意：并行执行应该比顺序执行快很多！
}

downloadFiles().then(() => {
  setTimeout(() => {
    console.log('✓ 测试完成');
    process.exit(0);
  }, 500);
});
