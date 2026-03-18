export interface Exercise {
  name: string;
  path: string;
  mode: 'test' | 'run';
  hint?: string;
}

export interface ExerciseResult {
  success: boolean;
  message: string;
  error?: string;
}

export interface Progress {
  completed: Set<string>;
  currentExercise: number;
}

export interface ExerciseConfig {
  exercises: Exercise[];
}
