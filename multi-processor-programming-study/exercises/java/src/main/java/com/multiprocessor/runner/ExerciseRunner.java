package com.multiprocessor.runner;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

/**
 * Exercise Runner - Rustlings-style exercise validator
 *
 * This runner helps you track your progress through the exercises.
 * It will:
 * 1. Check which exercises are complete
 * 2. Run tests for exercises
 * 3. Provide hints when you're stuck
 */
public class ExerciseRunner {

    private static final String RESET = "\u001B[0m";
    private static final String RED = "\u001B[31m";
    private static final String GREEN = "\u001B[32m";
    private static final String YELLOW = "\u001B[33m";
    private static final String BLUE = "\u001B[34m";
    private static final String CYAN = "\u001B[36m";

    private static class Exercise {
        String module;
        String name;
        String path;
        String testClass;
        boolean hasTodo;

        Exercise(String module, String name, String path, String testClass) {
            this.module = module;
            this.name = name;
            this.path = path;
            this.testClass = testClass;
            this.hasTodo = false;
        }
    }

    public static void main(String[] args) {
        System.out.println(CYAN + "╔═══════════════════════════════════════════════════════════╗" + RESET);
        System.out.println(CYAN + "║   Multi-Processor Programming Exercise Runner (Java)     ║" + RESET);
        System.out.println(CYAN + "╚═══════════════════════════════════════════════════════════╝" + RESET);
        System.out.println();

        if (args.length > 0) {
            String command = args[0];
            switch (command) {
                case "list":
                    listExercises();
                    break;
                case "verify":
                    if (args.length > 1) {
                        verifyExercise(args[1]);
                    } else {
                        verifyAll();
                    }
                    break;
                case "watch":
                    watchMode();
                    break;
                case "hint":
                    if (args.length > 1) {
                        showHint(args[1]);
                    }
                    break;
                default:
                    showHelp();
            }
        } else {
            showHelp();
            System.out.println();
            listExercises();
        }
    }

    private static void showHelp() {
        System.out.println("Usage: mvn exec:java -Dexec.args=\"<command> [options]\"");
        System.out.println();
        System.out.println("Commands:");
        System.out.println("  list              List all exercises and their status");
        System.out.println("  verify [name]     Verify an exercise or all exercises");
        System.out.println("  watch             Watch mode - automatically verify on file changes");
        System.out.println("  hint <name>       Show hints for a specific exercise");
        System.out.println();
        System.out.println("Examples:");
        System.out.println("  mvn exec:java -Dexec.args=\"list\"");
        System.out.println("  mvn exec:java -Dexec.args=\"verify counter\"");
        System.out.println("  mvn test -Dtest=CounterTest");
    }

    private static void listExercises() {
        System.out.println(BLUE + "📚 Available Exercises:" + RESET);
        System.out.println();

        String[] modules = {
            "01_basics", "02_mutual_exclusion", "03_concurrent_objects",
            "04_foundations", "05_synchronization", "06_consensus",
            "07_spin_locks", "08_monitors", "09_linked_lists",
            "10_queues", "11_stacks"
        };

        for (String module : modules) {
            System.out.println(YELLOW + "  " + module.replace("_", " ").toUpperCase() + RESET);
            System.out.println("    (Exercises will be listed here as they are created)");
            System.out.println();
        }

        System.out.println(CYAN + "💡 Tip: Start with 01_basics and work your way up!" + RESET);
    }

    private static void verifyExercise(String name) {
        System.out.println("Verifying exercise: " + name);
        System.out.println("Run: mvn test -Dtest=" + name + "Test");
    }

    private static void verifyAll() {
        System.out.println("Verifying all exercises...");
        System.out.println("Run: mvn test");
    }

    private static void watchMode() {
        System.out.println(GREEN + "🔍 Watch mode - monitoring for changes..." + RESET);
        System.out.println("Press Ctrl+C to exit");
    }

    private static void showHint(String name) {
        System.out.println(YELLOW + "💡 Hint for " + name + ":" + RESET);
        System.out.println("Check the comments in the exercise file for guidance!");
    }
}
