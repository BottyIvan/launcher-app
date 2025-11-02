# Contributing to Launcher

Thank you for your interest in contributing to Launcher! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Guidelines](#code-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)
- [Communication](#communication)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be:

- **Respectful**: Treat everyone with respect and kindness
- **Collaborative**: Work together and help each other
- **Professional**: Keep discussions focused and constructive
- **Inclusive**: Welcome contributors of all backgrounds and experience levels

Unacceptable behavior includes harassment, discrimination, trolling, or any form of abuse. Violations may result in removal from the project.

For more details, see [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.11+** installed
- **Git** for version control
- **GTK4** development libraries
- Basic knowledge of Python and GTK

### How You Can Contribute

There are many ways to contribute:

1. **Report bugs** - Found an issue? Let us know!
2. **Suggest features** - Have an idea? We'd love to hear it!
3. **Improve documentation** - Help make docs clearer
4. **Write code** - Fix bugs or implement features
5. **Review pull requests** - Help review contributions
6. **Test releases** - Try out new versions and provide feedback

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/launcher-app.git
cd launcher-app

# Add upstream remote
git remote add upstream https://github.com/BottyIvan/launcher-app.git
```

### 2. Install Dependencies

**System Dependencies (Ubuntu/Debian):**
```bash
sudo apt install \
    python3 \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    gir1.2-adwaita-1 \
    libgtk-4-dev \
    libadwaita-1-dev
```

**System Dependencies (Fedora):**
```bash
sudo dnf install \
    python3 \
    python3-pip \
    python3-gobject \
    gtk4 \
    libadwaita \
    gtk4-devel \
    libadwaita-devel
```

**System Dependencies (Arch Linux):**
```bash
sudo pacman -S \
    python \
    python-pip \
    python-gobject \
    gtk4 \
    libadwaita
```

**Python Dependencies:**
```bash
pip3 install --user PyGObject google-generativeai
```

### 3. Install Development Tools

```bash
# Code formatting
pip3 install black

# Linting
pip3 install flake8

# Type checking
pip3 install mypy

# Testing (built-in, but useful)
# python3 -m unittest is sufficient
```

### 4. Verify Setup

```bash
# Run the application
python3 -m cloud.ivanbotty.Launcher

# Run tests
python3 -m unittest discover tests/ -v

# Check code style
flake8 cloud/ivanbotty

# Format code
black --line-length 100 cloud/ivanbotty
```

## Development Workflow

### 1. Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add docstrings and type hints
- Keep changes focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
python3 -m unittest discover tests/ -v

# Run specific test
python3 -m unittest tests.test_utils.TestAppInitUtils

# Manual testing
python3 -m cloud.ivanbotty.Launcher
```

### 4. Format and Lint

```bash
# Format code
black --line-length 100 cloud/ivanbotty

# Check style
flake8 cloud/ivanbotty

# Type checking
mypy cloud/ivanbotty
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "Add feature: description of changes"

# Or for bug fixes
git commit -m "Fix: brief description of fix"
```

**Commit Message Guidelines:**
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep first line under 72 characters
- Add detailed description if needed
- Reference issue numbers when applicable

**Examples:**
```
Add math service with expression evaluation

Implements MathService class that safely evaluates mathematical
expressions without using eval(). Supports basic operators and
common functions like sqrt, sin, cos.

Closes #42
```

```
Fix: application search case sensitivity

Application search was case-sensitive, making it difficult to find
apps. Changed to case-insensitive matching for better UX.

Fixes #38
```

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
# Provide clear description of changes
```

## Code Guidelines

### Python Style

Follow **PEP 8** conventions with these specifics:

#### Line Length
```python
# Maximum line length: 100 characters
max_line_length = 100
```

#### Imports
```python
# Standard library imports first
import os
import sys
from typing import List, Optional

# Third-party imports
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

# Local imports last
from cloud.ivanbotty.Launcher.services import ApplicationsService
from cloud.ivanbotty.database.sqlite3 import Database
```

#### Type Hints
```python
# Always use type hints for function signatures
def search_applications(query: str, limit: int = 50) -> List[Application]:
    """Search for applications matching query."""
    pass

# Use type hints for class attributes
class ApplicationsService:
    _cache: Dict[str, Application]
    _db: Database
```

#### Docstrings
```python
def calculate(self, expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression as string
    
    Returns:
        float: Result of evaluation
    
    Raises:
        ValueError: If expression is invalid
    
    Example:
        >>> service.calculate("2 + 2")
        4.0
    """
    pass
```

#### Naming Conventions
```python
# Classes: PascalCase
class ApplicationsService:
    pass

# Functions and methods: snake_case
def search_applications():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RESULTS = 50

# Private: prefix with underscore
def _internal_helper():
    pass
```

### Code Organization

#### Module Structure
```python
"""Module docstring describing purpose."""

# Imports
import os
from typing import List

# Constants
DEFAULT_VALUE = 10

# Classes
class MyClass:
    """Class docstring."""
    pass

# Functions
def my_function():
    """Function docstring."""
    pass
```

#### Class Structure
```python
class MyClass:
    """Class docstring."""
    
    # Class attributes
    class_var: str = "value"
    
    def __init__(self):
        """Initialize instance."""
        # Instance attributes
        self.instance_var: int = 0
    
    # Public methods
    def public_method(self):
        """Public method."""
        pass
    
    # Private methods
    def _private_method(self):
        """Private helper method."""
        pass
    
    # Special methods
    def __str__(self) -> str:
        """String representation."""
        return f"MyClass({self.instance_var})"
```

### GTK/UI Code Guidelines

```python
# Use proper GTK object initialization
class MyWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self._build_ui()
    
    def _build_ui(self):
        """Build widget UI."""
        # Clear separation of UI building
        pass

# Connect signals properly
button.connect("clicked", self._on_button_clicked)

def _on_button_clicked(self, button):
    """Handle button click."""
    pass
```

## Testing Guidelines

### Writing Tests

```python
import unittest
from cloud.ivanbotty.Launcher.services.math_service import MathService

class TestMathService(unittest.TestCase):
    """Test suite for MathService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = MathService()
    
    def test_basic_calculation(self):
        """Test basic arithmetic."""
        result = self.service.calculate("2 + 2")
        self.assertEqual(result, 4.0)
    
    def test_invalid_expression(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            self.service.calculate("invalid")
```

### Test Coverage

Aim for:
- **Unit tests** for all services and utilities
- **Integration tests** for handler chains
- **Edge case testing** for error conditions
- Minimum **70% code coverage** for new code

### Running Tests

```bash
# All tests
python3 -m unittest discover tests/ -v

# Specific test file
python3 -m unittest tests.test_utils

# Specific test class
python3 -m unittest tests.test_utils.TestAppInitUtils

# Specific test method
python3 -m unittest tests.test_utils.TestAppInitUtils.test_import_app_init_module
```

## Submitting Changes

### Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure tests pass**
   ```bash
   python3 -m unittest discover tests/ -v
   ```

3. **Format code**
   ```bash
   black --line-length 100 cloud/ivanbotty
   flake8 cloud/ivanbotty
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create pull request**
   - Go to GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All tests pass
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Docstrings added/updated
- [ ] Type hints included
- [ ] Documentation updated if needed
- [ ] No breaking changes (or documented)

## Related Issues
Closes #(issue number)
```

### Review Process

1. **Automated checks** run (tests, linting)
2. **Maintainer review** - may request changes
3. **Address feedback** - make requested changes
4. **Approval** - once approved, will be merged
5. **Merge** - maintainer merges PR

## Project Structure

Understanding the project structure helps you navigate:

```
launcher-app/
├── cloud/ivanbotty/
│   ├── Launcher/          # Main application
│   │   ├── services/      # Business logic
│   │   ├── handlers/      # Input processing
│   │   ├── widget/        # UI components
│   │   ├── controller/    # Event controllers
│   │   ├── models/        # Data models
│   │   └── helper/        # Utilities
│   ├── Wizard/            # Welcome wizard
│   ├── database/          # Database layer
│   └── utils/             # Shared utilities
├── tests/                 # Test suite
├── wiki/                  # Documentation
└── ...
```

See [Architecture](Architecture.md) for detailed design information.

## Communication

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Pull Requests**: For code discussions
- **Email**: droidbotty@gmail.com for private inquiries

### Reporting Bugs

When reporting bugs, include:
1. **Description**: What happened vs. what you expected
2. **Steps to reproduce**: Exact steps to trigger bug
3. **Environment**: OS, Python version, GTK version
4. **Logs**: Relevant error messages or logs
5. **Screenshots**: If UI-related

### Suggesting Features

When suggesting features:
1. **Use case**: Why is this feature needed?
2. **Description**: What should the feature do?
3. **Alternatives**: Have you considered alternatives?
4. **Implementation ideas**: Optional, but helpful

## Additional Resources

- [Architecture Documentation](Architecture.md)
- [API Reference](API-Reference.md)
- [Development Guide](Usage-Guide.md)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [PyGObject Documentation](https://pygobject.readthedocs.io/)

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Project documentation

Thank you for contributing to Launcher! 🎉
