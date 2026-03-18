// 练习 29: 任务调度器 - 答案
//
// 实现一个任务调度器，支持定时执行、重复执行、任务依赖

interface Task {
  id: string;
  fn: () => Promise<any>;
  schedule?: {
    type: 'once' | 'interval' | 'cron';
    delay?: number; // 延迟（毫秒）
    interval?: number; // 间隔（毫秒）
  };
  dependencies?: string[]; // 依赖的任务 ID
  retry?: number;
}

interface TaskResult {
  id: string;
  success: boolean;
  result?: any;
  error?: string;
  executedAt: Date;
}

// 实现任务调度器
class TaskScheduler {
  private tasks: Map<string, Task> = new Map();
  private results: Map<string, TaskResult[]> = new Map();
  private running: Set<string> = new Set();
  private timers: Map<string, NodeJS.Timeout> = new Map();

  // 注册任务
  register(task: Task): void {
    this.tasks.set(task.id, task);
    if (!this.results.has(task.id)) {
      this.results.set(task.id, []);
    }
  }

  // 执行单个任务
  async executeTask(taskId: string): Promise<TaskResult> {
    const task = this.tasks.get(taskId);

    // 1. 检查任务是否存在
    if (!task) {
      throw new Error(`任务不存在: ${taskId}`);
    }

    // 2. 检查依赖任务是否已完成
    if (task.dependencies && task.dependencies.length > 0) {
      for (const depId of task.dependencies) {
        const depResults = this.results.get(depId);
        if (!depResults || depResults.length === 0) {
          const error = `依赖任务未完成: ${depId}`;
          const result: TaskResult = {
            id: taskId,
            success: false,
            error,
            executedAt: new Date(),
          };
          this.results.get(taskId)?.push(result);
          return result;
        }
        // 检查依赖任务是否成功
        const lastDepResult = depResults[depResults.length - 1];
        if (!lastDepResult.success) {
          const error = `依赖任务失败: ${depId}`;
          const result: TaskResult = {
            id: taskId,
            success: false,
            error,
            executedAt: new Date(),
          };
          this.results.get(taskId)?.push(result);
          return result;
        }
      }
    }

    // 3. 标记为运行中
    this.running.add(taskId);

    let lastError: Error | null = null;
    const maxRetries = task.retry || 0;

    // 4. 实现重试机制
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const taskResult = await task.fn();

        // 执行成功
        const result: TaskResult = {
          id: taskId,
          success: true,
          result: taskResult,
          executedAt: new Date(),
        };

        this.results.get(taskId)?.push(result);
        this.running.delete(taskId);
        return result;
      } catch (error) {
        lastError = error as Error;
        // 如果不是最后一次尝试，等待一会儿再重试
        if (attempt < maxRetries) {
          await new Promise((resolve) => setTimeout(resolve, 100 * (attempt + 1)));
        }
      }
    }

    // 所有重试都失败了
    const result: TaskResult = {
      id: taskId,
      success: false,
      error: lastError?.message || '未知错误',
      executedAt: new Date(),
    };

    this.results.get(taskId)?.push(result);
    this.running.delete(taskId);
    return result;
  }

  // 启动调度器
  start(): void {
    for (const [taskId, task] of this.tasks) {
      if (!task.schedule) continue;

      const { type, delay = 0, interval = 0 } = task.schedule;

      if (type === 'once') {
        // 延迟后执行一次
        const timer = setTimeout(() => {
          this.executeTask(taskId);
          this.timers.delete(taskId);
        }, delay);
        this.timers.set(taskId, timer);
      } else if (type === 'interval') {
        // 每隔一段时间执行
        const timer = setInterval(() => {
          // 如果任务还在运行中，跳过这次执行
          if (!this.running.has(taskId)) {
            this.executeTask(taskId);
          }
        }, interval);
        this.timers.set(taskId, timer);
      }
    }
  }

  // 停止调度器
  stop(): void {
    // 清除所有定时器
    for (const [taskId, timer] of this.timers) {
      clearTimeout(timer);
      clearInterval(timer);
    }
    this.timers.clear();
  }

  // 获取任务结果
  getResults(taskId: string): TaskResult[] {
    return this.results.get(taskId) || [];
  }

  // 获取调度器状态
  getStatus() {
    return {
      totalTasks: this.tasks.size,
      runningTasks: this.running.size,
      scheduledTasks: this.timers.size,
    };
  }
}

// 测试代码
async function testTaskScheduler() {
  const scheduler = new TaskScheduler();

  console.log('注册任务...\n');

  // 任务 1: 立即执行一次
  scheduler.register({
    id: 'task1',
    fn: async () => {
      console.log('任务 1 执行');
      return 'Task 1 完成';
    },
    schedule: {
      type: 'once',
      delay: 100,
    },
  });

  // 任务 2: 依赖任务 1
  scheduler.register({
    id: 'task2',
    fn: async () => {
      console.log('任务 2 执行（依赖任务 1）');
      return 'Task 2 完成';
    },
    dependencies: ['task1'],
  });

  // 任务 3: 每秒执行一次
  scheduler.register({
    id: 'task3',
    fn: async () => {
      console.log('任务 3 执行（定期任务）');
      return 'Task 3 完成';
    },
    schedule: {
      type: 'interval',
      interval: 1000,
    },
  });

  console.log('启动调度器...\n');
  scheduler.start();

  // 手动执行任务 2（会检查依赖）
  setTimeout(async () => {
    console.log('\n手动执行任务 2...');
    await scheduler.executeTask('task2');
  }, 500);

  // 3 秒后停止
  setTimeout(() => {
    console.log('\n停止调度器...');
    scheduler.stop();

    console.log('\n任务结果:');
    ['task1', 'task2', 'task3'].forEach((taskId) => {
      const results = scheduler.getResults(taskId);
      console.log(`\n${taskId}:`);
      results.forEach((r, i) => {
        console.log(`  ${i + 1}. ${r.success ? '✓' : '✗'} ${r.result || r.error}`);
      });
    });

    const status = scheduler.getStatus();
    console.log('\n调度器状态:');
    console.log(`  总任务数: ${status.totalTasks}`);
    console.log(`  运行中: ${status.runningTasks}`);
    console.log(`  已调度: ${status.scheduledTasks}`);

    console.log('\n✓ 测试完成');
    process.exit(0);
  }, 3000);
}

testTaskScheduler();
