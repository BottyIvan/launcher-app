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
- [blueprint-compiler](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/) (optional, for UI development)

## Getting Started

### Local Installation

```bash
pip install .
python -m cloud.ivanbotty.Launcher
```

### Running Directly Without Installation

You can run the application directly without installation:

```bash
# From the project root
python3 -m cloud.ivanbotty.Launcher
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

## UI Development with GTK Blueprint

Launcher uses [GTK Blueprint](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/) for declarative UI design. Blueprint files (`.blp`) are compiled to GTK UI files (`.ui`) that are loaded at runtime.

### Blueprint Files

Blueprint files are located in the `ui/` directory:
- `ui/main_window.blp` - Main application window layout
- `ui/search_entry.blp` - Search entry widget
- `ui/list_row.blp` - Application list row template
- `ui/footer.blp` - Footer with preferences and shortcuts
- `ui/preferences.blp` - Preferences dialog

### Installing blueprint-compiler

To edit and compile Blueprint files, you need `blueprint-compiler`:

**Ubuntu/Debian:**
```bash
sudo apt install blueprint-compiler
```

**Fedora:**
```bash
sudo dnf install blueprint-compiler
```

**Arch Linux:**
```bash
sudo pacman -S blueprint-compiler
```

**macOS (Homebrew):**
```bash
brew install blueprint-compiler
```

**From Flatpak:**
```bash
flatpak install flathub com.github.jwestman.blueprint-compiler
flatpak run com.github.jwestman.blueprint-compiler --help
```

### Compiling Blueprint Files

#### Method 1: Using the Python Script (Recommended for standalone use)

```bash
# Compile all Blueprint files
python3 compile_blueprints.py
```

This script will:
- Find all `.blp` files in the `ui/` directory
- Compile each to a `.ui` file using `blueprint-compiler`
- Report any compilation errors

#### Method 2: Using Meson (For integrated builds)

```bash
# Setup build directory
meson setup builddir

# Compile Blueprint files
meson compile -C builddir
```

#### Method 3: Manual Compilation

```bash
# Compile a single Blueprint file
blueprint-compiler compile --output ui/main_window.ui ui/main_window.blp

# Compile all files
for blp in ui/*.blp; do
    blueprint-compiler compile --output "${blp%.blp}.ui" "$blp"
done
```

### Using Blueprint Templates in Python

The compiled UI files can be loaded using `Gtk.Template`. See `examples_blueprint.py` for complete examples:

```python
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'main_window.ui'))
class MyWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LauncherWindow'
    
    # Bind widgets from the UI file
    search_entry = Gtk.Template.Child()
    list_view = Gtk.Template.Child()
    
    def __init__(self, application):
        super().__init__(application=application)
        # Widgets are now accessible as self.search_entry, self.list_view, etc.
```

### Workflow for UI Changes

1. **Edit Blueprint files** in `ui/*.blp`
2. **Compile** using `python3 compile_blueprints.py` or meson
3. **Test** by running the application
4. **Commit** both `.blp` and `.ui` files (or just `.blp` if configured in CI)

### Blueprint Syntax Resources

- [Blueprint Tutorial](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/tutorial.html)
- [Blueprint Syntax Reference](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/reference.html)
- [GTK4 Widget Gallery](https://docs.gtk.org/gtk4/visual_index.html)
- [Libadwaita Widget Gallery](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/widget-gallery.html)

---

## Project Structure

- `cloud/ivanbotty/database/`: SQLite integration for persistent data
- `cloud/ivanbotty/Launcher/`: Main source code
- `cloud/ivanbotty/Wizard/`: Wizard/Onboard source code
- `resources/`: SVG icons and appdata files
- `ui/`: GTK Blueprint UI files (.blp) and compiled UI files (.ui)
- `manifest.yaml`: Flatpak manifest
- `pyproject.toml`: Python configuration
- `meson.build`: Build configuration for compiling Blueprint files
- `compile_blueprints.py`: Standalone script to compile Blueprint files

## Contributing

Fork the repository and submit a pull request. Follow PEP8 conventions and ensure your code is tested.

## License

GPL-3.0-or-later