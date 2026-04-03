# Contributing to YPT

Thank you for considering contributing to YPT (Your Packet Tracer)! 🎉

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Your environment**: Linux distro, desktop environment, Python version
- **Debug output**: Run with `ypt --debug` and include `~/.local/share/PacketTracer/debug.log`

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case** - Why is this enhancement useful?
- **Detailed description** of the proposed functionality
- **Alternative solutions** you've considered
- **Mockups or examples** if applicable

### Pull Requests

1. **Fork** the repository and create your branch from `main`
2. **Make your changes**:
   - Follow PEP 8 style guidelines
   - Add docstrings to new functions/classes
   - Add type hints where appropriate
   - Update documentation if needed
3. **Add tests** - Ensure your changes are tested
4. **Run the test suite**: `pytest`
5. **Ensure tests pass** and coverage doesn't decrease
6. **Commit** with clear, descriptive commit messages
7. **Push** to your fork and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/itxmjr/ypt.git
cd ypt

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=ypt --cov-report=html
```

## Style Guidelines

### Python Code

- Follow **PEP 8** style guide
- Use **type hints** for function arguments and return values
- Write **docstrings** for all public functions, classes, and modules
- Keep functions focused and small (ideally < 50 lines)
- Use descriptive variable names

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add support for detecting Brave browser

- Checks for brave-browser and brave-browser-stable executables
- Adds test coverage for Brave detection
- Updates documentation with Brave in browser list

Fixes #123
```

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage (target: 80%+)
- Use pytest fixtures for common test setup
- Mock external dependencies (filesystem, subprocess, etc.)
- Test edge cases and error conditions

## Project Structure

```
ypt/
├── ypt/                    # Main package
│   ├── __init__.py
│   ├── cli.py             # CLI entry point
│   ├── config.py          # Configuration and constants
│   ├── deb_extractor.py   # .deb extraction logic
│   ├── appimage_installer.py  # AppImage installation
│   ├── browser_detector.py    # Browser detection
│   ├── launcher_generator.py  # Wrapper script generation
│   ├── url_handler_shim.py   # URL handler shim
│   ├── desktop_integration.py # .desktop file integration
│   └── debug.py           # Diagnostics and debugging
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   └── test_*.py          # Test modules
├── pyproject.toml         # Package configuration
└── README.md              # Documentation
```

## Testing Your Changes

### Unit Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_browser_detector.py

# Run with coverage
pytest --cov=ypt --cov-report=term-missing
```

### Manual Testing

```bash
# Test installation with a real .deb file
ypt /path/to/CiscoPacketTracer.deb

# Test browser detection
ypt --test-browser

# Test diagnostics
ypt --diagnose

# Test uninstallation
ypt --uninstall
```

## Release Process

Maintainers follow this process for releases:

1. Update version in `pyproject.toml` and `ypt/__init__.py`
2. Update `CHANGELOG.md` with release notes
3. Create a git tag: `git tag -a v1.x.x -m "Release v1.x.x"`
4. Push tag: `git push origin v1.x.x`
5. Build package: `python -m build`
6. Upload to PyPI: `twine upload dist/*`
7. Create GitHub release from tag

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

## License

By contributing to YPT, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to YPT!** 🚀
