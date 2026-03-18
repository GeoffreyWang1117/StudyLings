# Rustlings Suite

**14 interactive self-study projects, 854 exercises, one unified framework.**

Learn by doing — fill in the blanks, fix the code, watch it pass. Inspired by [Rust Rustlings](https://github.com/rust-lang/rustlings).

🌐 **[Live Demo Page](https://geoffreywang1117.github.io/rustlings-suite/)**

## Projects

| Project | Exercises | Language | Topic |
|---------|-----------|----------|-------|
| **Algolings** | 132 | Python | GC, concurrency, crypto, compilers, ML |
| **Cudalings** | 105 | CUDA C++ | GPU programming: kernels to ray tracing |
| **Economlings** | 100 | Python | Economics: micro, macro, finance, behavioral |
| **Physics Rustlings** | 100 | Python | Classical mechanics to quantum field theory |
| **Genlings** | 68 | Python | GenAI: Transformers, GANs, Diffusion, CLIP |
| **ADM Algorithms** | 68 | C++ | Algorithm Design Manual exercises |
| **Sutton RL** | 54 | Python | Reinforcement learning: bandits to RLHF |
| **ODS Rustlings** | 48 | Python | Data structures: arrays, trees, graphs |
| **Debuglings** | 39 | C | GDB/LLDB debugging techniques |
| **Quantumlings** | 34 | Python | Quantum computing with Qiskit |
| **Asynclings** | 30 | TypeScript | Async programming: Promises, async/await |
| **JAXlings** | 30 | Python | JAX framework and neural networks |
| **MPlings** | 26 | C++ | Multi-processor concurrent programming |
| **Vulkanlings** | 20 | C++ | Vulkan graphics API |

## Quick Start

```bash
git clone https://github.com/GeoffreyWang1117/rustlings-suite.git
cd rustlings-suite
pip install -e .

# Pick a project
cd Gen-AI-Study
python -m genailings          # show status + next exercise
python -m genailings watch    # auto-rerun on file save
```

## Unified CLI

Every project responds to the same 9 commands:

```
<tool> list [--chapter CH]     # Browse exercises by chapter
<tool> run [name]              # Run specific exercise (or next)
<tool> next                    # Run next incomplete exercise
<tool> verify [name]           # Validate one or all exercises
<tool> watch [name]            # Watch mode with auto-advance
<tool> hint <name> [--level N] # Progressive hints
<tool> progress                # Per-chapter progress bars
<tool> solution <name>         # View reference answer
<tool> reset [--all]           # Reset progress
```

## Suite Dashboard

```bash
cd rustlings-suite
python -m studylings           # aggregate progress across all 14 projects
```

## Architecture

```
rustlings-suite/
├── studylings/              # Shared core framework
│   ├── cli.py               # 9 unified Click commands
│   ├── exercise.py          # Discovery & metadata (.py/.cpp/.cu/.ts/.c)
│   ├── checker.py           # 3 pluggable validators
│   ├── progress.py          # Unified JSON progress tracking
│   ├── watcher.py           # File watch with auto-advance
│   └── ui.py                # Rich terminal output
│
├── Gen-AI-Study/            # Each project = thin config wrapper
│   ├── genailings/
│   │   ├── config.py        # ProjectConfig(name, chapters, mode, ...)
│   │   └── __main__.py      # → studylings.cli.main(config)
│   └── exercises/           # Exercise files unchanged
│
├── ... 13 more projects ...
└── docs/index.html          # GitHub Pages site
```

### Validation Modes

| Mode | How it works | Used by |
|------|-------------|---------|
| `test_file` | External test files validate functions | Economlings |
| `verify_func` | Embedded `verify()` + `# I AM NOT DONE` markers | 9 projects |
| `compile_and_run` | Check markers → cmake/make → execute | C/C++/CUDA projects |

## Adding a New Project

1. Create `<your_project>/<package>/config.py` with a `ProjectConfig`
2. Create `<your_project>/<package>/__main__.py` that calls `studylings.cli.main(config)`
3. Add exercises to `<your_project>/exercises/<chapter>/`
4. Done — your project gets all 9 CLI commands automatically
