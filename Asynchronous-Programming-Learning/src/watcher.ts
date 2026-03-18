import chokidar from 'chokidar';
import { Exercise } from './types';
import { runExercise } from './runner';
import { markComplete, loadProgress } from './progress';
import { exercises } from './config';
import { printExerciseResult, printProgress } from './ui';

export async function watchExercises(): Promise<void> {
  console.log('👀 监控模式已启动...\n');
  console.log('修改练习文件后会自动运行测试');
  console.log('按 Ctrl+C 退出\n');

  const progress = loadProgress();

  // 找到第一个未完成的练习
  let currentExercise = exercises.find(
    (ex) => !progress.completed.has(ex.name)
  );

  if (!currentExercise) {
    console.log('🎉 恭喜！你已经完成了所有练习！');
    return;
  }

  console.log(`📝 当前练习: ${currentExercise.name}`);
  console.log(`📁 文件: ${currentExercise.path}\n`);

  if (currentExercise.hint) {
    console.log(`💡 提示: ${currentExercise.hint}\n`);
  }

  // 监控当前练习文件
  const watcher = chokidar.watch(currentExercise.path, {
    persistent: true,
    ignoreInitial: false,
  });

  watcher.on('change', async () => {
    console.clear();
    console.log(`🔄 检测到文件变化...\n`);
    console.log(`📝 练习: ${currentExercise!.name}`);
    console.log(`📁 文件: ${currentExercise!.path}\n`);

    const result = await runExercise(currentExercise!);
    printExerciseResult(result);

    if (result.success) {
      markComplete(currentExercise!.name);
      const updatedProgress = loadProgress();

      // 关闭当前监控
      await watcher.close();

      // 找到下一个练习
      const nextExercise = exercises.find(
        (ex) => !updatedProgress.completed.has(ex.name)
      );

      if (nextExercise) {
        console.log(`\n✨ 准备下一个练习...\n`);
        currentExercise = nextExercise;
        console.log(`📝 当前练习: ${currentExercise.name}`);
        console.log(`📁 文件: ${currentExercise.path}\n`);

        if (currentExercise.hint) {
          console.log(`💡 提示: ${currentExercise.hint}\n`);
        }

        // 监控新的练习文件
        watcher.add(currentExercise.path);
      } else {
        console.log('\n🎉 恭喜！你已经完成了所有练习！');
        printProgress();
        process.exit(0);
      }
    }
  });

  // 初始运行一次
  const result = await runExercise(currentExercise);
  printExerciseResult(result);

  if (result.success) {
    markComplete(currentExercise.name);
    const updatedProgress = loadProgress();
    const nextExercise = exercises.find(
      (ex) => !updatedProgress.completed.has(ex.name)
    );

    if (nextExercise) {
      await watcher.close();
      currentExercise = nextExercise;
      console.log(`\n📝 下一个练习: ${currentExercise.name}`);
      console.log(`📁 文件: ${currentExercise.path}\n`);
      if (currentExercise.hint) {
        console.log(`💡 提示: ${currentExercise.hint}\n`);
      }
      watcher.add(currentExercise.path);
    }
  }
}
