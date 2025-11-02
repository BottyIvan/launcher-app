# Launcher

> [!IMPORTANT]
> **Launcher** is under active development. Features and interfaces may change frequently. Contributions and feedback are welcome!

<p align="center">
    <img src="./cloud/ivanbotty/Launcher/resources/cloud.ivanbotty.Launcher.svg" alt="Launcher Icon" width="96">
</p>

**Launcher** is a modern desktop application launcher for Linux, built with GTK4 and Adwaita. It offers instant search, a sleek user interface, and seamless integration for launching installed applications. The extension system allows you to add new features and customize your workflow.

<p align="center">
    <video src="./assets/launcher.mp4" controls width="480">
        Your browser does not support the video tag.
    </video>
</p>

> Icon rights: [Icons8](https://icons8.it/icon/qW0hxm9M3J5x/ricerca)

---

## Features

- Modern interface with Adwaita and GTK4
- Flatpak support for sandboxed environments
- Switchable compact and extended layouts
- SVG icon rendering and detailed app info
- Persistent user preferences (SQLite)
- Extension system for enabling/disabling features
- Type-annotated codebase for better IDE support
- Comprehensive test suite

### Core Services

- **ApplicationsService**
    - Discovers installed apps from `.desktop` files
    - Instant search and filtering by name
    - Dynamic, ordered app list via `Gio.ListStore`

- **ExtensionService**
    - Manage extensions: add, remove, enable, disable
    - Search and list extensions by name
    - Extensions can register custom services

- **CommandService**
    - Execute commands linked to applications for fast launching *(in development)*

- **MathService**
    - Built-in calculator for mathematical expressions

- **AIService**
    - Integration with AI APIs for natural language queries *(in development)*

### Extensions

Launcher supports extensions defined in YAML, which can be enabled or disabled from the preferences. Available extensions include:

- Application search
- Math calculator
- Command runner *(in development)*
- AI assistant (Gemini) *(in development)*
- File manager *(in development)*
- Link management *(in development)*

---

## Requirements

- Python >= 3.11
- [PyGObject](https://pygobject.readthedocs.io/en/latest/) >= 3.44
- [google-generativeai](https://pypi.org/project/google-generativeai/) >= 0.3.0 (for AI features)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) (built-in with Python)
- GTK4 and Adwaita libraries
- Meson >= 0.59.0 (for building with Meson)

## Getting Started

Launcher is distributed via Flatpak, which provides a sandboxed environment with all dependencies included.

### Install and Run with Flatpak

```bash
# Build and install Launcher with Flatpak
flatpak-builder --user --install --force-clean build-dir manifest.yaml

# Launch the application
flatpak run cloud.ivanbotty.Launcher
```

### Development Setup

To contribute to Launcher or run it from source:

```bash
# Clone the repository
git clone https://github.com/BottyIvan/launcher-app.git
cd launcher-app

# Install development dependencies (optional but recommended)
python3 -m pip install black flake8 mypy

# Run the application directly
python3 -m cloud.ivanbotty.Launcher

# Or run the welcome wizard
python3 -m cloud.ivanbotty.Wizard
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests/

# Run specific test file
python3 -m unittest tests/test_utils.py

# Run with verbose output
python3 -m unittest discover tests/ -v
```

---

## Project Structure

- `cloud/ivanbotty/database/`: Persistent data management with SQLite
    - `sqlite3.py`: Database and preferences handling with type hints
    - `__init__.py`
- `cloud/ivanbotty/utils/`: Shared utility modules
    - `app_init.py`: App initialization (resources, DB, logging)
    - `__init__.py`
- `cloud/ivanbotty/Launcher/`: Main Launcher app code
    - `app.py`, `__main__.py`: Entry point and core logic
    - `config/`: UI configurations and constants
    - `controller/`: Event controllers (search, key, click)
    - `handlers/`: Input handling (app, math, AI, link, command, extensions)
    - `helper/`: Utilities (parser, thread manager, dynamic loader)
    - `models/`: Data models (applications, extensions)
    - `services/`: Services (applications, command, math, AI, extensions)
    - `widget/`: UI components (window, search_entry, row, preferences, progress_bar, footer)
    - `resources/`: SVG icons, appdata, extension YAML, wizard files
- `cloud/ivanbotty/Wizard/`: Wizard/onboarding source code
    - `app.py`, `__main__.py`: Welcome wizard
    - `components/`: Wizard UI components
- `tests/`: Test suite
    - `test_utils.py`: Utility module tests
    - `test_helpers.py`: Helper module tests
- `manifest.yaml`: Flatpak manifest
- `pyproject.toml`: Python configuration
- `meson.build`: Meson build configuration
- `cloud.ivanbotty.Launcher.desktop`: Desktop entry for Launcher
- `launcher-wrapper.sh.in`: Launcher wrapper script
- `LICENSE`: GPL-3.0-or-later

## Contributing

We welcome contributions! Here's how to get started:

### Code Style

- Follow PEP8 conventions
- Use type hints for function signatures
- Add docstrings to modules, classes, and functions
- Format code with `black --line-length 100`
- Check code with `flake8`

### Workflow

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the code style guidelines
4. **Write or update tests** for your changes
5. **Run tests** to ensure everything works: `python3 -m unittest discover tests/`
6. **Format your code**: `black cloud/ivanbotty --line-length 100`
7. **Commit your changes** with clear, descriptive messages
8. **Push** to your fork and **submit a pull request**

### Guidelines

- Keep changes focused and atomic
- Ensure backward compatibility when possible
- Update documentation for new features
- Add tests for new functionality
- Maintain consistent code style with existing codebase

## License

GPL-3.0-or-later