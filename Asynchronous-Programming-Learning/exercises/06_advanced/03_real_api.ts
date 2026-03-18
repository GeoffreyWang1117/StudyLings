// 练习 23: 真实场景 - API 调用
//
// 模拟真实的 REST API 调用场景

interface User {
  id: number;
  name: string;
  email: string;
}

interface Post {
  id: number;
  userId: number;
  title: string;
  content: string;
}

// 模拟 API 调用
function fetchUserById(userId: number): Promise<User> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (userId > 0 && userId <= 3) {
        resolve({
          id: userId,
          name: `User${userId}`,
          email: `user${userId}@example.com`,
        });
      } else {
        reject(new Error('用户不存在'));
      }
    }, 100);
  });
}

function fetchPostsByUser(userId: number): Promise<Post[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          id: 1,
          userId,
          title: `Post 1 by User ${userId}`,
          content: 'Content 1',
        },
        {
          id: 2,
          userId,
          title: `Post 2 by User ${userId}`,
          content: 'Content 2',
        },
      ]);
    }, 150);
  });
}

// TODO: 实现一个函数，获取用户信息和该用户的所有帖子
// 要求：
// 1. 先获取用户信息
// 2. 如果用户存在，再获取该用户的帖子
// 3. 返回包含用户和帖子的对象
// 4. 处理可能的错误
async function getUserWithPosts(userId: number): Promise<{
  user: User;
  posts: Post[];
} | null> {
  // 在这里实现代码
  return null;
}

// 测试代码
(async () => {
  console.log('获取用户 1 的信息和帖子...');
  const result1 = await getUserWithPosts(1);
  if (result1) {
    console.log('用户:', result1.user.name);
    console.log('帖子数量:', result1.posts.length);
  }

  console.log('\n尝试获取不存在的用户...');
  const result2 = await getUserWithPosts(999);
  console.log('结果:', result2);

  setTimeout(() => {
    console.log('\n✓ 测试完成');
    process.exit(0);
  }, 200);
})();
