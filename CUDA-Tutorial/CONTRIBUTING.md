# Contributing to JAXlings

Thank you for your interest in contributing to JAXlings!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs
- Provide clear description and steps to reproduce
- Include your Python and JAX versions

### Adding Exercises

1. Create a new exercise file in the appropriate directory
2. Follow the existing exercise format:
   - Start with docstring explaining the concept
   - Include `# I AM NOT DONE` marker
   - Provide clear TODO comments
   - Include comprehensive tests
   - Add helpful hints

3. Add the exercise to `exercises.toml`:
```toml
[[exercises]]
name = "your_exercise_name"
path = "exercises/XX_category/exercise_name.py"
mode = "test"
hint = """
Your hint here...
"""
```

4. Test your exercise:
```bash
python exercises/XX_category/exercise_name.py
jaxlings run your_exercise_name
```

### Improving Existing Exercises

- Make exercises clearer
- Add better hints
- Improve test coverage
- Fix bugs

### Code Style

- Follow PEP 8
- Use descriptive variable names
- Add docstrings to functions
- Keep exercises focused on one concept

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with clear description

## Questions?

Open an issue for discussion!

Thank you for contributing! 🎉
