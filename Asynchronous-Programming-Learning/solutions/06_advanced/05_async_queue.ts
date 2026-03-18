// 练习 25: 异步队列 - 答案

type AsyncTask<T> = () => Promise<T>;

class AsyncQueue {
  private queue: Array<{
    task: AsyncTask<any>;
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }> = [];
  private running: boolean = false;

  enqueue<T>(task: AsyncTask<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject });

      if (!this.running) {
        this.processQueue();
      }
    });
  }

  private async processQueue(): Promise<void> {
    if (this.running || this.queue.length === 0) {
      return;
    }

    this.running = true;

    while (this.queue.length > 0) {
      const item = this.queue.shift();

      if (item) {
        try {
          const result = await item.task();
          item.resolve(result);
        } catch (error) {
          item.reject(error);
        }
      }
    }

    this.running = false;
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

  const promise1 = queue.enqueue(createTask(1, 200));
  const promise2 = queue.enqueue(createTask(2, 100));
  const promise3 = queue.enqueue(createTask(3, 150));

  const results = await Promise.all([promise1, promise2, promise3]);

  console.log('\n所有任务结果:', results);
  console.log('✓ 测试完成');
  process.exit(0);
})();
