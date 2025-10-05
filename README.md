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

## Getting Started

### Local Installation

```bash
pip install .
python -m cloud.ivanbotty.Launcher
```

### Flatpak

> [!WARNING]
> **Note:** Application icons may not display correctly in Flatpak due to sandboxing.

Build and run with Flatpak:

```bash
flatpak-builder build-dir manifest.yaml --force-clean
flatpak-builder --run build-dir manifest.yaml launcher
```

---

## Project Structure

- `cloud/ivanbotty/database/`: SQLite integration for persistent data
- `cloud/ivanbotty/Launcher/`: Main source code
- `resources/`: SVG icons and appdata files
- `manifest.yaml`: Flatpak manifest
- `pyproject.toml`: Python configuration

## Contributing

Fork the repository and submit a pull request. Follow PEP8 conventions and ensure your code is tested.

## License

GPL-3.0-or-later