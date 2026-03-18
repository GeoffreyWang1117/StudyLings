import * as fs from 'fs';
import * as path from 'path';
import { Progress } from './types';

const PROGRESS_FILE = path.join(process.cwd(), '.progress.json');

export function loadProgress(): Progress {
  try {
    if (fs.existsSync(PROGRESS_FILE)) {
      const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8'));
      return {
        completed: new Set(data.completed || []),
        currentExercise: data.currentExercise || 0,
      };
    }
  } catch (error) {
    // 如果读取失败，返回默认进度
  }

  return {
    completed: new Set(),
    currentExercise: 0,
  };
}

export function saveProgress(progress: Progress): void {
  const data = {
    completed: Array.from(progress.completed),
    currentExercise: progress.currentExercise,
  };

  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data, null, 2));
}

export function markComplete(exerciseName: string): void {
  const progress = loadProgress();
  progress.completed.add(exerciseName);
  saveProgress(progress);
}

export function resetProgress(): void {
  if (fs.existsSync(PROGRESS_FILE)) {
    fs.unlinkSync(PROGRESS_FILE);
  }
}
