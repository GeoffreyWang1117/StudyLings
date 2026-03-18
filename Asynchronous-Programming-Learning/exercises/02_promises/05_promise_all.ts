// 练习 8: Promise.all() 并行执行
//
// Promise.all() 接收一个 Promise 数组，等待所有 Promise 完成
// 所有 Promise 都成功时返回结果数组，任一失败则整体失败

function fetchUser(id: number): Promise<{ id: number; name: string }> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id, name: `User${id}` });
    }, 100);
  });
}

// TODO: 使用 Promise.all() 并行获取三个用户（id: 1, 2, 3）的数据
// 然后打印 "Users: <所有用户名，用逗号分隔>"
async function fetchAllUsers() {
  // 在这里实现代码
  // 提示：Promise.all([fetchUser(1), fetchUser(2), fetchUser(3)])
}

fetchAllUsers();

// 验证：应该输出 "Users: User1, User2, User3"
setTimeout(() => {
  console.log('✓ 测试完成');
  process.exit(0);
}, 300);
