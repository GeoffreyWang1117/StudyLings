#!/usr/bin/env node

import { Command } from 'commander';
import { watchExercises } from './watcher';
import { runExercise, checkExercise } from './runner';
import { exercises } from './config';
import { loadProgress, markComplete, resetProgress } from './progress';
import {
  printExerciseResult,
  printProgress,
  listExercises,
  printHint,
  printWelcome,
} from './ui';
import chalk from 'chalk';

const program = new Command();

program
  .name('async-learnings')
  .description('TypeScript 异步编程学习框架')
  .version('1.0.0');

program
  .command('watch')
  .description('监控模式，自动运行当前练习')
  .action(async () => {
    await watchExercises();
  });

program
  .command('run [exercise]')
  .description('运行指定练习（或当前练习）')
  .action(async (exerciseName?: string) => {
    const progress = loadProgress();

    let exercise;

    if (exerciseName) {
      exercise = exercises.find((ex) => ex.name === exerciseName);
      if (!exercise) {
        console.log(chalk.red(`练习 ${exerciseName} 不存在`));
        process.exit(1);
      }
    } else {
      // 运行第一个未完成的练习
      exercise = exercises.find((ex) => !progress.completed.has(ex.name));

      if (!exercise) {
        console.log(chalk.green('🎉 所有练习都已完成！'));
        process.exit(0);
      }
    }

    console.log(chalk.bold(`\n📝 运行练习: ${exercise.name}\n`));
    const result = await runExercise(exercise);
    printExerciseResult(result);

    if (result.success) {
      markComplete(exercise.name);
      printProgress();
    } else if (exercise.hint) {
      console.log(chalk.yellow(`\n💡 提示: ${exercise.hint}`));
    }
  });

program
  .command('verify')
  .description('验证所有练习')
  .action(async () => {
    console.log(chalk.bold('\n🔍 验证所有练习...\n'));

    let passCount = 0;
    let failCount = 0;

    for (const exercise of exercises) {
      process.stdout.write(`${exercise.name}... `);

      const result = await runExercise(exercise);

      if (result.success) {
        console.log(chalk.green('✓'));
        passCount++;
        markComplete(exercise.name);
      } else {
        console.log(chalk.red('✗'));
        failCount++;

        if (result.error) {
          console.log(chalk.red(`  ${result.message}`));
        }
      }
    }

    console.log(
      chalk.bold(
        `\n结果: ${chalk.green(passCount + ' 通过')}, ${chalk.red(failCount + ' 失败')}`
      )
    );
    printProgress();
  });

program
  .command('list')
  .description('列出所有练习')
  .action(() => {
    listExercises();
  });

program
  .command('reset')
  .description('重置学习进度')
  .action(() => {
    resetProgress();
    console.log(chalk.yellow('\n🔄 学习进度已重置'));
  });

program
  .command('hint [exercise]')
  .description('显示练习提示')
  .action((exerciseName?: string) => {
    const progress = loadProgress();

    if (!exerciseName) {
      // 显示当前练习的提示
      const currentExercise = exercises.find(
        (ex) => !progress.completed.has(ex.name)
      );

      if (!currentExercise) {
        console.log(chalk.green('所有练习都已完成！'));
        return;
      }

      exerciseName = currentExercise.name;
    }

    printHint(exerciseName);
  });

program
  .command('solution [exercise]')
  .description('查看练习答案')
  .action((exerciseName?: string) => {
    const progress = loadProgress();
    const fs = require('fs');
    const path = require('path');

    if (!exerciseName) {
      const currentExercise = exercises.find(
        (ex) => !progress.completed.has(ex.name)
      );

      if (!currentExercise) {
        console.log(chalk.green('所有练习都已完成！'));
        return;
      }

      exerciseName = currentExercise.name;
    }

    const exercise = exercises.find((ex) => ex.name === exerciseName);

    if (!exercise) {
      console.log(chalk.red(`练习 ${exerciseName} 不存在`));
      return;
    }

    // 构建答案文件路径
    const solutionPath = exercise.path.replace('exercises/', 'solutions/');

    if (!fs.existsSync(solutionPath)) {
      console.log(chalk.yellow(`答案文件不存在: ${solutionPath}`));
      return;
    }

    console.log(chalk.bold(`\n📖 ${exercise.name} 的答案:\n`));
    console.log(chalk.gray(`文件: ${solutionPath}\n`));
    console.log(chalk.yellow('提示: 先自己尝试完成练习，再查看答案！\n'));
    console.log(
      chalk.cyan(
        `运行答案: ${chalk.white(`npx tsx ${solutionPath}`)}\n`
      )
    );
  });

program
  .command('next')
  .description('跳到下一个练习')
  .action(() => {
    const progress = loadProgress();
    const currentExercise = exercises.find(
      (ex) => !progress.completed.has(ex.name)
    );

    if (!currentExercise) {
      console.log(chalk.green('🎉 所有练习都已完成！'));
      return;
    }

    // 标记当前练习为完成
    markComplete(currentExercise.name);
    console.log(
      chalk.yellow(`⏭️  跳过练习: ${currentExercise.name}`)
    );

    const updatedProgress = loadProgress();
    const nextExercise = exercises.find(
      (ex) => !updatedProgress.completed.has(ex.name)
    );

    if (nextExercise) {
      console.log(
        chalk.cyan(`\n📝 下一个练习: ${nextExercise.name}`)
      );
      console.log(chalk.gray(`📁 文件: ${nextExercise.path}`));

      if (nextExercise.hint) {
        console.log(chalk.yellow(`\n💡 提示: ${nextExercise.hint}`));
      }
    } else {
      console.log(chalk.green('\n🎉 所有练习都已完成！'));
    }

    printProgress();
  });

// 默认显示欢迎信息
if (process.argv.length === 2) {
  printWelcome();
  listExercises();
} else {
  program.parse();
}
