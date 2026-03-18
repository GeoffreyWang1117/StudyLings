// 练习 9: Promise.race() 竞速 - 答案

function fastOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('快速操作完成'), 100);
  });
}

function slowOperation(): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve('慢速操作完成'), 500);
  });
}

async function raceOperations() {
  const winner = await Promise.race([
    fastOperation(),
    slowOperation(),
  ]);

  console.log(`Winner: ${winner}`);
}

raceOperations();

setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 300);
