import chalk from 'chalk';
import { Exercise, ExerciseResult } from './types';
import { loadProgress } from './progress';
import { exercises } from './config';

export function printExerciseResult(result: ExerciseResult): void {
  if (result.success) {
    console.log(chalk.green.bold('✓ 成功！') + ' ' + result.message);
  } else {
    console.log(chalk.red.bold('✗ 失败') + ' ' + result.message);
    if (result.error) {
      console.log(chalk.red('\n错误信息:'));
      console.log(chalk.gray(result.error));
    }
  }
}

export function printProgress(): void {
  const progress = loadProgress();
  const total = exercises.length;
  const completed = progress.completed.size;
  const percentage = Math.round((completed / total) * 100);

  console.log('\n' + chalk.bold('学习进度:'));
  console.log(
    `${chalk.green('●'.repeat(completed))}${chalk.gray('○'.repeat(total - completed))} ${completed}/${total} (${percentage}%)`
  );
}

export function listExercises(): void {
  const progress = loadProgress();

  console.log(chalk.bold('\n📚 练习列表:\n'));

  let currentSection = '';

  exercises.forEach((exercise, index) => {
    const section = exercise.path.split('/')[1];

    if (section !== currentSection) {
      currentSection = section;
      const sectionName = {
        '01_basics': '基础概念',
        '02_promises': 'Promise 基础',
        '03_async_await': 'async/await',
        '04_error_handling': '错误处理',
        '05_concurrent': '并发控制',
        '06_advanced': '进阶主题',
        '07_applications': '实战应用',
      }[section] || section;

      console.log(chalk.cyan.bold(`\n${sectionName}:`));
    }

    const isCompleted = progress.completed.has(exercise.name);
    const status = isCompleted ? chalk.green('✓') : chalk.gray('○');
    const name = isCompleted
      ? chalk.gray(exercise.name)
      : chalk.white(exercise.name);

    console.log(`  ${status} ${name}`);
  });

  printProgress();
}

export function printHint(exerciseName: string): void {
  const exercise = exercises.find((ex) => ex.name === exerciseName);

  if (!exercise) {
    console.log(chalk.red(`练习 ${exerciseName} 不存在`));
    return;
  }

  console.log(chalk.bold(`\n💡 ${exercise.name} 的提示:\n`));

  if (exercise.hint) {
    console.log(chalk.yellow(exercise.hint));
  } else {
    console.log(chalk.gray('这个练习没有提示'));
  }

  console.log(chalk.gray(`\n文件路径: ${exercise.path}`));
}

export function printWelcome(): void {
  console.log(chalk.bold.cyan('\n🚀 欢迎来到 Async Learnings!\n'));
  console.log('这是一个类似 rustlings 的 TypeScript 异步编程学习框架\n');
  console.log(chalk.bold('📚 共 30 个练习，涵盖从基础到实战应用的异步编程知识\n'));
  console.log(chalk.bold('可用命令:'));
  console.log('  ' + chalk.green('npm run watch   ') + ' - 监控模式，自动运行测试（推荐）');
  console.log('  ' + chalk.green('npm run list    ') + ' - 查看所有练习和进度');
  console.log('  ' + chalk.green('npm run run     ') + ' - 运行当前练习');
  console.log('  ' + chalk.green('npm run verify  ') + ' - 验证所有练习');
  console.log('  ' + chalk.green('npm run hint    ') + ' - 显示当前练习提示');
  console.log('  ' + chalk.green('npm run solution') + ' - 查看当前练习答案');
  console.log('  ' + chalk.green('npm run next    ') + ' - 跳到下一个练习');
  console.log('  ' + chalk.green('npm run reset   ') + ' - 重置学习进度');
  console.log('\n' + chalk.bold('📖 文档:'));
  console.log('  ' + chalk.cyan('docs/GUIDE.md     ') + ' - 详细的学习指南');
  console.log('  ' + chalk.cyan('docs/SOLUTIONS.md ') + ' - 答案使用说明');
  console.log('  ' + chalk.cyan('docs/UTILS.md     ') + ' - 工具函数库文档');
  console.log('\n' + chalk.yellow('💡 提示: 运行 ') + chalk.green('npm run watch') + chalk.yellow(' 开始学习！\n'));
}
