import { spawn } from 'child_process';
import { Exercise, ExerciseResult } from './types';
import * as fs from 'fs';

export async function runExercise(exercise: Exercise): Promise<ExerciseResult> {
  // 检查文件是否存在
  if (!fs.existsSync(exercise.path)) {
    return {
      success: false,
      message: `练习文件不存在: ${exercise.path}`,
    };
  }

  // 读取文件内容检查是否包含 TODO 标记
  const content = fs.readFileSync(exercise.path, 'utf-8');
  const todoPattern = /\/\/\s*TODO|\/\/\s*FIXME|\/\/\s*待完成/i;

  if (todoPattern.test(content)) {
    return {
      success: false,
      message: '请完成代码中的 TODO 标记',
      error: '代码中仍有未完成的部分',
    };
  }

  return new Promise((resolve) => {
    const child = spawn('tsx', [exercise.path], {
      stdio: 'pipe',
      cwd: process.cwd(),
    });

    let stdout = '';
    let stderr = '';

    child.stdout?.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr?.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve({
          success: true,
          message: '✓ 练习通过！',
        });
      } else {
        resolve({
          success: false,
          message: '✗ 练习失败',
          error: stderr || stdout,
        });
      }
    });

    child.on('error', (error) => {
      resolve({
        success: false,
        message: '✗ 执行错误',
        error: error.message,
      });
    });
  });
}

export function checkExercise(exercise: Exercise): { hasIssue: boolean; message?: string } {
  if (!fs.existsSync(exercise.path)) {
    return {
      hasIssue: true,
      message: `文件不存在: ${exercise.path}`,
    };
  }

  const content = fs.readFileSync(exercise.path, 'utf-8');
  const todoPattern = /\/\/\s*TODO|\/\/\s*FIXME|\/\/\s*待完成/i;

  if (todoPattern.test(content)) {
    return {
      hasIssue: true,
      message: '包含未完成的 TODO 标记',
    };
  }

  return { hasIssue: false };
}
