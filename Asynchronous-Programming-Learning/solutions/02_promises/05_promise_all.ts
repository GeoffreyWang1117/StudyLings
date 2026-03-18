// 练习 8: Promise.all() 并行执行 - 答案

function fetchUser(id: number): Promise<{ id: number; name: string }> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id, name: `User${id}` });
    }, 100);
  });
}

async function fetchAllUsers() {
  const users = await Promise.all([
    fetchUser(1),
    fetchUser(2),
    fetchUser(3),
  ]);

  const userNames = users.map((u) => u.name).join(', ');
  console.log(`Users: ${userNames}`);
}

fetchAllUsers();

setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 300);
