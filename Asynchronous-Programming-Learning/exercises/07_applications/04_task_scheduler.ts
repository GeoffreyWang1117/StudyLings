// 练习 29: 任务调度器
//
// 【学习目标】
// 在这个练习中，你将实现一个任务调度器，学习：
// 1. 定时任务 - 延迟执行和周期执行
// 2. 任务依赖 - 确保依赖任务先完成
// 3. 状态管理 - 跟踪任务执行状态和结果
// 4. 定时器管理 - 创建和清理定时器
//
// 【核心概念】
// - setTimeout：延迟执行一次
// - setInterval：周期性执行
// - 依赖检查：验证前置任务是否完成
// - 执行历史：记录每次执行的结果
//
// 【实现提示】
// 1. register()：注册任务
//    - 保存到 tasks Map
//    - 初始化 results 数组
// 2. executeTask()：执行任务
//    - 检查任务是否存在
//    - 检查依赖任务是否完成（results 中有成功记录）
//    - 执行任务（支持重试）
//    - 记录结果
// 3. start()：启动调度器
//    - 遍历所有任务
//    - 根据 schedule 类型创建定时器
//    - once: setTimeout
//    - interval: setInterval（注意避免重复执行）
// 4. stop()：停止调度器
//    - 清除所有定时器
//
// 【预期行为】
// - 定时任务按时执行
// - 有依赖的任务会检查依赖状态
// - 周期任务会重复执行
// - 可以手动执行任务
// - 停止后所有定时器清除

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

// TODO: 实现任务调度器
class TaskScheduler {
  private tasks: Map<string, Task> = new Map();
  private results: Map<string, TaskResult[]> = new Map();
  private running: Set<string> = new Set();
  private timers: Map<string, NodeJS.Timeout> = new Map();

  // TODO: 注册任务
  register(task: Task): void {
    // 实现步骤：
    // 1. 保存任务：this.tasks.set(task.id, task)
    // 2. 初始化结果数组：
    //    if (!this.results.has(task.id)) {
    //      this.results.set(task.id, [])
    //    }
    throw new Error('未实现');
  }

  // TODO: 执行单个任务
  async executeTask(taskId: string): Promise<TaskResult> {
    // 实现步骤：
    // 1. 获取任务：const task = this.tasks.get(taskId)
    //    - 如果不存在，抛出错误
    // 2. 检查依赖（如果有 dependencies）：
    //    - 遍历每个依赖 ID
    //    - 获取依赖任务的结果：const depResults = this.results.get(depId)
    //    - 如果没有结果或最后一次失败，返回失败结果
    // 3. 标记运行中：this.running.add(taskId)
    // 4. 实现重试（类似前面练习）：
    //    - for 循环（0 到 task.retry || 0）
    //    - try { 执行 task.fn() } catch { 记录错误，等待后重试 }
    // 5. 记录结果：this.results.get(taskId)?.push(result)
    // 6. 清除运行标记：this.running.delete(taskId)
    // 7. 返回结果

    throw new Error('未实现');
  }

  // TODO: 启动调度器
  start(): void {
    // 实现步骤：
    // 遍历所有任务：for (const [taskId, task] of this.tasks)
    //   - 如果没有 schedule，跳过
    //   - 根据 schedule.type 创建定时器：
    //
    //     1. 'once' 类型：
    //        const timer = setTimeout(() => {
    //          this.executeTask(taskId)
    //          this.timers.delete(taskId)  // 执行后删除
    //        }, task.schedule.delay || 0)
    //        this.timers.set(taskId, timer)
    //
    //     2. 'interval' 类型：
    //        const timer = setInterval(() => {
    //          if (!this.running.has(taskId)) {  // 避免重复执行
    //            this.executeTask(taskId)
    //          }
    //        }, task.schedule.interval || 1000)
    //        this.timers.set(taskId, timer)

    throw new Error('未实现');
  }

  // TODO: 停止调度器
  stop(): void {
    // 实现步骤：
    // 1. 遍历所有定时器：for (const [taskId, timer] of this.timers)
    // 2. 清除定时器：clearTimeout(timer) 和 clearInterval(timer) 都能清除
    // 3. 清空 Map：this.timers.clear()
    throw new Error('未实现');
  }

  // TODO: 获取任务结果
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
