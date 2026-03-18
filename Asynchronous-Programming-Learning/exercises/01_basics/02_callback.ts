// 练习 2: 回调函数
//
// 回调函数是异步编程的基础。回调函数就是传递给另一个函数的函数，
// 当某个操作完成时被调用。

// 模拟一个异步操作（比如从服务器获取数据）
function fetchUserData(userId: number, callback: (user: { id: number; name: string }) => void) {
  setTimeout(() => {
    const user = { id: userId, name: `User${userId}` };
    callback(user);
  }, 100);
}

// TODO: 实现这个函数，使用 fetchUserData 获取用户数据，
// 然后在回调中打印 "User name: <name>"
function printUserName(userId: number) {
  // 在这里实现代码
}

// 测试代码
console.log('开始获取用户数据...');
printUserName(123);

// 验证：运行后应该输出 "User name: User123"
