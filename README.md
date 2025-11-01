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

You can run Launcher in three ways: via Flatpak (recommended for users), Meson build (recommended for system installation), or direct Python execution (recommended for development).

### Method 1: 🧱 Build and Run with Flatpak (Recommended for Users)

Flatpak provides a sandboxed environment with all dependencies included. To build and install:

```bash
# Build and install the Flatpak
flatpak-builder --user --install --force-clean build-dir manifest.yaml

# Run the application
flatpak run cloud.ivanbotty.Launcher
```

The Flatpak build uses Meson internally and installs the application to `/app` with proper sandboxing and permissions.

### Method 2: Meson Build (Recommended for System Installation)

Build and install using Meson:

```bash
# Setup the build directory
meson setup builddir

# Install to the system (may require sudo)
meson install -C builddir

# Run the installed application
cloud-ivanbotty-launcher
```

To install to a custom prefix (e.g., in your home directory):

```bash
meson setup builddir --prefix=$HOME/.local
meson install -C builddir
# Make sure $HOME/.local/bin is in your PATH
cloud-ivanbotty-launcher
```

### Method 3: Direct Python Execution (For Development)

Run directly without installation:

```bash
# Install Python dependencies
pip install PyGObject google-generativeai

# Run the application
python3 -m cloud.ivanbotty.Launcher
```

---

## Project Structure

- `cloud/ivanbotty/database/`: SQLite integration for persistent data
    - `sqlite3.py`: Database and preferences management
    - `__init__.py`
- `cloud/ivanbotty/Launcher/`: Main source code
    - `app.py`, `__main__.py`: Entry point and main logic
    - `config/`: UI configurations and constants
    - `controller/`: Event controllers (search, key, click)
    - `handlers/`: Input handling (app, math, AI, link, command, extensions)
    - `helper/`: Utilities (parser, thread manager, dynamic loader)
    - `models/`: Data models (applications, extensions)
    - `services/`: Services (applications, command, math, AI, extensions)
    - `widget/`: UI components (window, search_entry, row, preferences, progress_bar, footer)
    - `resources/`: SVG icons, appdata, extension YAMLs, and wizard files
        - `cloud.ivanbotty.Launcher.svg`
        - `appdata.xml`
        - `extensions.yaml`
        - `wizard.yaml`
        - `resources.gresource`
        - `resources.xml`
- `cloud/ivanbotty/Wizard/`: Wizard/Onboarding source code
    - `app.py`, `__main__.py`: Welcome wizard
    - `components/`: UI components for the wizard
- `manifest.yaml`: Flatpak manifest
- `pyproject.toml`: Python configuration
- `meson.build`: Meson build configuration
- `cloud.ivanbotty.Launcher.desktop`: Desktop entry for the launcher
- `launcher-wrapper.sh.in`: Launcher wrapper script
- `LICENSE`: GPL license

## Contributing

Fork the repository and submit a pull request. Follow PEP8 conventions and ensure your code is tested.

## License

GPL-3.0-or-later