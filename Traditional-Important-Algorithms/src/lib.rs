use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Deserialize)]
pub struct Exercise {
    pub name: String,
    pub path: String,
    pub mode: String,
    pub hint: String,
}

#[derive(Debug, Deserialize)]
pub struct ExerciseList {
    pub exercises: Vec<Exercise>,
}

impl ExerciseList {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string("info.toml")?;
        let list: ExerciseList = toml::from_str(&content)?;
        Ok(list)
    }
}

pub fn verify_exercise(exercise: &Exercise) -> Result<bool, Box<dyn std::error::Error>> {
    let output = std::process::Command::new("rustc")
        .args(&["--test", &exercise.path, "-o", "/tmp/exercise_test"])
        .output()?;

    if !output.status.success() {
        return Ok(false);
    }

    let test_output = std::process::Command::new("/tmp/exercise_test").output()?;

    Ok(test_output.status.success())
}

pub fn get_exercise_status(exercise: &Exercise) -> ExerciseStatus {
    let content = match fs::read_to_string(&exercise.path) {
        Ok(c) => c,
        Err(_) => return ExerciseStatus::Missing,
    };

    if content.contains("I AM NOT DONE") {
        ExerciseStatus::Pending
    } else {
        match verify_exercise(exercise) {
            Ok(true) => ExerciseStatus::Done,
            Ok(false) => ExerciseStatus::Failed,
            Err(_) => ExerciseStatus::Failed,
        }
    }
}

#[derive(Debug, PartialEq)]
pub enum ExerciseStatus {
    Pending,
    Done,
    Failed,
    Missing,
}
