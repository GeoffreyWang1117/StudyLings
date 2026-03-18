# Contributing to Traditional Important Algorithms

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in Issues
- Include steps to reproduce the bug
- Specify which exercise is affected
- Include error messages if applicable

### Suggesting Enhancements

- Clearly describe the enhancement
- Explain why it would be useful
- Provide examples if possible

### Adding New Exercises

When adding new exercises, please ensure:

1. **Follow the format**: Use existing exercises as templates
2. **Include tests**: Comprehensive test coverage is required
3. **Add to info.toml**: Register the exercise with appropriate metadata
4. **Write clear documentation**: Explain the algorithm and what students should learn
5. **Use TODO markers**: Guide students through the implementation
6. **Include hints**: Add helpful hints in info.toml

### Exercise Format Checklist

- [ ] File starts with clear documentation
- [ ] Includes "I AM NOT DONE" marker
- [ ] Has TODO comments guiding implementation
- [ ] Contains comprehensive tests (minimum 5)
- [ ] Tests cover edge cases
- [ ] Registered in info.toml with name, path, mode, and hint
- [ ] Follows Rust naming conventions
- [ ] Code is well-commented

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-exercise`
3. Make your changes
4. Run tests: `cargo test`
5. Update documentation if needed
6. Commit with clear messages
7. Push to your fork
8. Submit a pull request

### Code Style

- Follow Rust standard formatting: `cargo fmt`
- Run clippy: `cargo clippy`
- Keep line length reasonable (< 100 chars)
- Use meaningful variable names
- Comment non-obvious logic

## Questions?

Feel free to open an issue for any questions or discussions!

Thank you for contributing! 🎉
