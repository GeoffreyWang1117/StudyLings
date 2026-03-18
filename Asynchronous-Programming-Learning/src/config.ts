import { Exercise } from './types';

export const exercises: Exercise[] = [
  // 01. 基础概念
  { name: '01_intro', path: 'exercises/01_basics/01_intro.ts', mode: 'run', hint: '理解什么是异步编程，以及为什么需要它' },
  { name: '02_callback', path: 'exercises/01_basics/02_callback.ts', mode: 'test', hint: '回调函数是异步编程的基础' },
  { name: '03_callback_hell', path: 'exercises/01_basics/03_callback_hell.ts', mode: 'test', hint: '体验回调地狱的问题' },

  // 02. Promise 基础
  { name: '04_promise_intro', path: 'exercises/02_promises/01_promise_intro.ts', mode: 'test', hint: 'Promise 代表一个异步操作的最终完成或失败' },
  { name: '05_promise_then', path: 'exercises/02_promises/02_promise_then.ts', mode: 'test', hint: '使用 .then() 处理 Promise 的成功结果' },
  { name: '06_promise_catch', path: 'exercises/02_promises/03_promise_catch.ts', mode: 'test', hint: '使用 .catch() 处理 Promise 的错误' },
  { name: '07_promise_chain', path: 'exercises/02_promises/04_promise_chain.ts', mode: 'test', hint: 'Promise 链式调用可以避免回调地狱' },
  { name: '08_promise_all', path: 'exercises/02_promises/05_promise_all.ts', mode: 'test', hint: 'Promise.all() 并行执行多个 Promise' },
  { name: '09_promise_race', path: 'exercises/02_promises/06_promise_race.ts', mode: 'test', hint: 'Promise.race() 返回最快完成的 Promise' },

  // 03. async/await
  { name: '10_async_intro', path: 'exercises/03_async_await/01_async_intro.ts', mode: 'test', hint: 'async 函数总是返回一个 Promise' },
  { name: '11_await_basic', path: 'exercises/03_async_await/02_await_basic.ts', mode: 'test', hint: 'await 会暂停执行直到 Promise 完成' },
  { name: '12_async_sequential', path: 'exercises/03_async_await/03_async_sequential.ts', mode: 'test', hint: '顺序执行异步操作' },
  { name: '13_async_parallel', path: 'exercises/03_async_await/04_async_parallel.ts', mode: 'test', hint: '使用 Promise.all() 并行执行' },

  // 04. 错误处理
  { name: '14_try_catch', path: 'exercises/04_error_handling/01_try_catch.ts', mode: 'test', hint: '使用 try/catch 捕获异步错误' },
  { name: '15_error_propagation', path: 'exercises/04_error_handling/02_error_propagation.ts', mode: 'test', hint: '错误会在 Promise 链中传播' },
  { name: '16_finally', path: 'exercises/04_error_handling/03_finally.ts', mode: 'test', hint: 'finally 总是会执行，无论成功或失败' },

  // 05. 并发控制
  { name: '17_concurrent_limit', path: 'exercises/05_concurrent/01_concurrent_limit.ts', mode: 'test', hint: '限制并发数量避免资源耗尽' },
  { name: '18_promise_allsettled', path: 'exercises/05_concurrent/02_promise_allsettled.ts', mode: 'test', hint: 'allSettled 等待所有 Promise 完成，无论成功或失败' },
  { name: '19_retry_mechanism', path: 'exercises/05_concurrent/03_retry_mechanism.ts', mode: 'test', hint: '实现重试机制处理临时性失败' },
  { name: '20_timeout', path: 'exercises/05_concurrent/04_timeout.ts', mode: 'test', hint: '为异步操作设置超时' },

  // 06. 进阶主题
  { name: '21_event_loop', path: 'exercises/06_advanced/01_event_loop.ts', mode: 'run', hint: '理解 Event Loop、微任务和宏任务的执行顺序' },
  { name: '22_async_iterator', path: 'exercises/06_advanced/02_async_iterator.ts', mode: 'test', hint: '使用异步迭代器处理异步数据流' },
  { name: '23_real_api', path: 'exercises/06_advanced/03_real_api.ts', mode: 'test', hint: '模拟真实的 API 调用场景' },
  { name: '24_debounce_throttle', path: 'exercises/06_advanced/04_debounce_throttle.ts', mode: 'test', hint: '实现防抖和节流优化频繁操作' },
  { name: '25_async_queue', path: 'exercises/06_advanced/05_async_queue.ts', mode: 'test', hint: '实现异步任务队列' },

  // 07. 实战应用
  { name: '26_http_client', path: 'exercises/07_applications/01_http_client.ts', mode: 'test', hint: '封装 HTTP 客户端，应用缓存、重试、超时等技术' },
  { name: '27_connection_pool', path: 'exercises/07_applications/02_connection_pool.ts', mode: 'test', hint: '实现数据库连接池，管理有限资源' },
  { name: '28_file_processor', path: 'exercises/07_applications/03_file_processor.ts', mode: 'test', hint: '批量处理文件，控制并发和进度' },
  { name: '29_task_scheduler', path: 'exercises/07_applications/04_task_scheduler.ts', mode: 'test', hint: '实现任务调度器，支持定时和依赖' },
  { name: '30_rate_limiter', path: 'exercises/07_applications/05_rate_limiter.ts', mode: 'test', hint: '实现限流器，控制请求频率' },
];
