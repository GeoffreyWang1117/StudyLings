// 练习 2: 回调函数 - 答案

function fetchUserData(userId: number, callback: (user: { id: number; name: string }) => void) {
  setTimeout(() => {
    const user = { id: userId, name: `User${userId}` };
    callback(user);
  }, 100);
}

function printUserName(userId: number) {
  fetchUserData(userId, (user) => {
    console.log(`User name: ${user.name}`);
  });
}

console.log('开始获取用户数据...');
printUserName(123);
