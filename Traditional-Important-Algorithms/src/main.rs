use clap::{Parser, Subcommand};
use colored::*;
use indicatif::{ProgressBar, ProgressStyle};
use std::process::Command;
use traditional_important_algorithms::*;

#[derive(Parser)]
#[command(name = "algorithms")]
#[command(about = "Interactive exercises for traditional and important algorithms", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Verify a specific exercise
    Verify { name: String },

    /// Watch an exercise and re-run on changes
    Watch { name: String },

    /// Run all exercises
    Run,

    /// Show a hint for an exercise
    Hint { name: String },

    /// List all exercises
    List,
}

fn main() {
    let cli = Cli::parse();

    let exercises = match ExerciseList::load() {
        Ok(list) => list.exercises,
        Err(e) => {
            eprintln!("{} Failed to load exercises: {}", "ERROR:".red().bold(), e);
            std::process::exit(1);
        }
    };

    match cli.command {
        Some(Commands::Verify { name }) => {
            verify_command(&exercises, &name);
        }
        Some(Commands::Watch { name }) => {
            watch_command(&exercises, &name);
        }
        Some(Commands::Run) => {
            run_command(&exercises);
        }
        Some(Commands::Hint { name }) => {
            hint_command(&exercises, &name);
        }
        Some(Commands::List) => {
            list_command(&exercises);
        }
        None => {
            println!("{}", "Welcome to Traditional Important Algorithms!".green().bold());
            println!("\nUse {} to see available commands.", "algorithms --help".yellow());
            println!("Use {} to list all exercises.", "algorithms list".yellow());
            println!("Use {} to verify an exercise.", "algorithms verify <name>".yellow());
        }
    }
}

fn verify_command(exercises: &[Exercise], name: &str) {
    let exercise = match exercises.iter().find(|e| e.name == name) {
        Some(ex) => ex,
        None => {
            eprintln!("{} Exercise '{}' not found", "ERROR:".red().bold(), name);
            return;
        }
    };

    println!("{} Verifying {}...", "INFO:".blue().bold(), exercise.name);

    match verify_exercise(exercise) {
        Ok(true) => {
            println!("{} {} passed all tests!", "SUCCESS:".green().bold(), exercise.name);
        }
        Ok(false) => {
            println!("{} {} failed tests", "FAILED:".red().bold(), exercise.name);
            println!("\n{} Run {} to see the hint", "HINT:".yellow().bold(),
                     format!("algorithms hint {}", name).cyan());
        }
        Err(e) => {
            eprintln!("{} Failed to verify: {}", "ERROR:".red().bold(), e);
        }
    }
}

fn watch_command(exercises: &[Exercise], name: &str) {
    let exercise = match exercises.iter().find(|e| e.name == name) {
        Some(ex) => ex,
        None => {
            eprintln!("{} Exercise '{}' not found", "ERROR:".red().bold(), name);
            return;
        }
    };

    println!("{} Watching {}. Press Ctrl+C to exit.", "INFO:".blue().bold(), exercise.name);
    println!("{} Modify the file and save to trigger verification.\n", "INFO:".blue().bold());

    // Simple watch loop
    loop {
        std::thread::sleep(std::time::Duration::from_secs(2));

        let status = get_exercise_status(exercise);
        if status == ExerciseStatus::Done {
            println!("\n{} {} is complete!", "SUCCESS:".green().bold(), exercise.name);
            break;
        }
    }
}

fn run_command(exercises: &[Exercise]) {
    println!("{} Running all exercises...\n", "INFO:".blue().bold());

    let pb = ProgressBar::new(exercises.len() as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("[{bar:40.cyan/blue}] {pos}/{len} {msg}")
            .unwrap()
            .progress_chars("=>-"),
    );

    let mut passed = 0;
    let mut failed = 0;
    let mut pending = 0;

    for exercise in exercises {
        pb.set_message(exercise.name.clone());

        match get_exercise_status(exercise) {
            ExerciseStatus::Done => {
                passed += 1;
                println!("  {} {}", "✓".green(), exercise.name);
            }
            ExerciseStatus::Pending => {
                pending += 1;
                println!("  {} {} (pending)", "○".yellow(), exercise.name);
            }
            ExerciseStatus::Failed => {
                failed += 1;
                println!("  {} {} (failed)", "✗".red(), exercise.name);
            }
            ExerciseStatus::Missing => {
                pending += 1;
                println!("  {} {} (missing)", "○".yellow(), exercise.name);
            }
        }

        pb.inc(1);
    }

    pb.finish_with_message("Complete");

    println!("\n{}", "Summary:".bold());
    println!("  {} Passed: {}", "✓".green(), passed);
    println!("  {} Failed: {}", "✗".red(), failed);
    println!("  {} Pending: {}", "○".yellow(), pending);

    if passed == exercises.len() {
        println!("\n{} All exercises complete! 🎉", "SUCCESS:".green().bold());
    }
}

fn hint_command(exercises: &[Exercise], name: &str) {
    let exercise = match exercises.iter().find(|e| e.name == name) {
        Some(ex) => ex,
        None => {
            eprintln!("{} Exercise '{}' not found", "ERROR:".red().bold(), name);
            return;
        }
    };

    println!("{} Hint for {}:", "HINT:".yellow().bold(), exercise.name);
    println!("\n{}", exercise.hint);
}

fn list_command(exercises: &[Exercise]) {
    println!("{}\n", "Available Exercises:".green().bold());

    let categories = vec![
        ("01_gc_and_memory", "🧩 Garbage Collection and Memory Management"),
        ("02_memory_models", "🧩 Memory Models and Safety Mechanisms"),
        ("03_concurrency", "🧩 Concurrency and Scheduling"),
        ("04_os_algorithms", "🧩 Operating System Algorithms"),
        ("05_compiler", "🧩 Compiler and Runtime Mechanisms"),
        ("06_distributed_systems", "🧩 Network and Distributed Systems"),
        ("07_cryptography", "🔐 Cryptography and Security"),
        ("08_database", "💾 Database and Storage"),
        ("09_rate_limiting", "🚦 Rate Limiting and Fault Tolerance"),
        ("10_string_algorithms", "📝 String and Text Processing"),
        ("11_stream_processing", "🌊 Stream Processing"),
        ("12_graph_algorithms", "🕸️ Graph Algorithms"),
        ("13_data_structures", "🌳 Data Structures"),
        ("14_ml_fundamentals", "🤖 Machine Learning Fundamentals"),
    ];

    for (category_path, category_name) in categories {
        println!("{}", category_name.cyan().bold());

        for exercise in exercises.iter().filter(|e| e.path.contains(category_path)) {
            let status = get_exercise_status(exercise);
            let status_icon = match status {
                ExerciseStatus::Done => "✓".green(),
                ExerciseStatus::Pending => "○".yellow(),
                ExerciseStatus::Failed => "✗".red(),
                ExerciseStatus::Missing => "?".yellow(),
            };

            println!("  {} {} - {}", status_icon, exercise.name, exercise.path);
        }

        println!();
    }
}
