// 练习 25: 异步队列
//
// 实现一个异步任务队列，按顺序执行异步任务

type AsyncTask<T> = () => Promise<T>;

// TODO: 实现一个异步队列类
class AsyncQueue {
  private queue: AsyncTask<any>[] = [];
  private running: boolean = false;

  // 添加任务到队列
  enqueue<T>(task: AsyncTask<T>): Promise<T> {
    // 在这里实现代码
    // 提示：返回一个 Promise，在任务执行完成时 resolve
    return Promise.resolve(undefined as any);
  }

  // 处理队列
  private async processQueue(): Promise<void> {
    // 在这里实现代码
    // 提示：循环处理队列中的任务，直到队列为空
  }
}

// 测试代码
const queue = new AsyncQueue();

function createTask(id: number, delay: number): AsyncTask<string> {
  return () =>
    new Promise((resolve) => {
      console.log(`任务 ${id} 开始`);
      setTimeout(() => {
        console.log(`任务 ${id} 完成`);
        resolve(`Result ${id}`);
      }, delay);
    });
}

(async () => {
  console.log('添加任务到队列...\n');

  // 添加多个任务
  const promise1 = queue.enqueue(createTask(1, 200));
  const promise2 = queue.enqueue(createTask(2, 100));
  const promise3 = queue.enqueue(createTask(3, 150));

  // 等待所有任务完成
  const results = await Promise.all([promise1, promise2, promise3]);

  console.log('\n所有任务结果:', results);
  console.log('✓ 测试完成');
  process.exit(0);
})();
