#!/usr/bin/env tsx

/**
 * 验证所有答案文件是否能正确运行
 */

import { spawn } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface TestResult {
  file: string;
  passed: boolean;
  error?: string;
  duration: number;
}

const SOLUTIONS_DIR = path.join(process.cwd(), 'solutions');
const TIMEOUT = 10000; // 10 秒超时

async function runSolution(filePath: string): Promise<TestResult> {
  const startTime = Date.now();

  return new Promise((resolve) => {
    const child = spawn('tsx', [filePath], {
      stdio: 'pipe',
      timeout: TIMEOUT,
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
      const duration = Date.now() - startTime;

      if (code === 0) {
        resolve({
          file: path.relative(process.cwd(), filePath),
          passed: true,
          duration,
        });
      } else {
        resolve({
          file: path.relative(process.cwd(), filePath),
          passed: false,
          error: stderr || stdout || `退出码: ${code}`,
          duration,
        });
      }
    });

    child.on('error', (error) => {
      const duration = Date.now() - startTime;
      resolve({
        file: path.relative(process.cwd(), filePath),
        passed: false,
        error: error.message,
        duration,
      });
    });
  });
}

function getAllSolutionFiles(dir: string): string[] {
  const files: string[] = [];

  function traverse(currentDir: string) {
    const items = fs.readdirSync(currentDir);

    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        traverse(fullPath);
      } else if (item.endsWith('.ts')) {
        files.push(fullPath);
      }
    }
  }

  traverse(dir);
  return files.sort();
}

async function main() {
  console.log('🔍 验证所有答案文件...\n');

  if (!fs.existsSync(SOLUTIONS_DIR)) {
    console.error('❌ solutions/ 目录不存在');
    process.exit(1);
  }

  const solutionFiles = getAllSolutionFiles(SOLUTIONS_DIR);

  if (solutionFiles.length === 0) {
    console.error('❌ 没有找到答案文件');
    process.exit(1);
  }

  console.log(`找到 ${solutionFiles.length} 个答案文件\n`);

  const results: TestResult[] = [];

  for (const file of solutionFiles) {
    const fileName = path.relative(SOLUTIONS_DIR, file);
    process.stdout.write(`测试 ${fileName}... `);

    const result = await runSolution(file);
    results.push(result);

    if (result.passed) {
      console.log(`✅ (${result.duration}ms)`);
    } else {
      console.log(`❌`);
    }
  }

  // 打印摘要
  console.log('\n' + '='.repeat(60));
  console.log('测试摘要');
  console.log('='.repeat(60) + '\n');

  const passed = results.filter((r) => r.passed);
  const failed = results.filter((r) => !r.passed);

  console.log(`总计: ${results.length}`);
  console.log(`✅ 通过: ${passed.length}`);
  console.log(`❌ 失败: ${failed.length}`);

  const totalDuration = results.reduce((sum, r) => sum + r.duration, 0);
  console.log(`⏱️  总耗时: ${totalDuration}ms`);

  // 显示失败的详情
  if (failed.length > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('失败的测试');
    console.log('='.repeat(60) + '\n');

    for (const result of failed) {
      console.log(`❌ ${result.file}`);
      if (result.error) {
        console.log(`   错误: ${result.error.split('\n')[0]}`);
      }
      console.log('');
    }
  }

  // 退出码
  process.exit(failed.length > 0 ? 1 : 0);
}

main().catch((error) => {
  console.error('验证过程出错:', error);
  process.exit(1);
});
