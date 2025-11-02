# Usage Guide

Learn how to use Launcher effectively to boost your productivity.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Search Features](#search-features)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [User Interface](#user-interface)
- [Extensions](#extensions)
- [Preferences](#preferences)
- [Tips & Tricks](#tips--tricks)

## Getting Started

### First Launch

When you first launch Launcher, you may see the Welcome Wizard:

```bash
# Launch the wizard
flatpak run cloud.ivanbotty.Launcher
# or
python3 -m cloud.ivanbotty.Wizard
```

The wizard will guide you through:
1. Initial setup
2. Extension configuration
3. Keyboard shortcut setup

### Quick Start

1. **Open Launcher**: Press your configured keyboard shortcut or click the application icon
2. **Type to Search**: Start typing the name of an application
3. **Select & Launch**: Use arrow keys or mouse to select, then press Enter or click

## Basic Usage

### Launching Applications

**Method 1: Keyboard**
1. Open Launcher
2. Type the application name (e.g., "firefox")
3. Use ↑/↓ arrow keys to navigate
4. Press Enter to launch

**Method 2: Mouse**
1. Open Launcher
2. Type the application name
3. Click on the desired application

### Application Search

Launcher performs **instant search** as you type:
- Search by application name
- Results appear immediately
- Fuzzy matching supported
- Case-insensitive search

**Example searches:**
- Type "fire" → finds Firefox
- Type "term" → finds Terminal, GNOME Terminal
- Type "edit" → finds Text Editor, VS Code

## Search Features

### Application Search

The default search mode finds installed applications:

```
Type: firefox
Results: Firefox, Firefox Developer Edition
```

### Math Calculator

Launcher includes a built-in calculator. Type mathematical expressions:

```
Type: 2 + 2
Result: 4

Type: sqrt(16)
Result: 4.0

Type: sin(pi/2)
Result: 1.0
```

**Supported operations:**
- Basic: `+`, `-`, `*`, `/`, `**` (power)
- Functions: `sqrt()`, `sin()`, `cos()`, `tan()`, `log()`, `abs()`
- Constants: `pi`, `e`
- Parentheses for order of operations

### Command Runner (In Development)

Execute system commands directly from Launcher:

```
Type: command: ls -la
```

### AI Assistant (In Development)

Ask questions using AI integration:

```
Type: ai: What is Python?
```

> **Note**: AI features require API configuration. See [Configuration](Configuration.md).

## Keyboard Shortcuts

### Navigation

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | Navigate results |
| `Enter` | Launch selected application |
| `Esc` | Close Launcher |
| `Tab` | Switch between compact/extended view |

### Search

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all text |
| `Ctrl+C` | Copy selected text |
| `Ctrl+V` | Paste |
| `Backspace` | Delete character |

### Window Management

| Shortcut | Action |
|----------|--------|
| `Alt+F4` | Close window |
| `F11` | Toggle fullscreen (if supported) |

## User Interface

### Compact Mode

The default view shows:
- Search bar at the top
- Application icons in a grid
- Application name below each icon

**Best for**: Quick launches with visual recognition

### Extended Mode

Toggle to extended mode for:
- List view with details
- Application descriptions
- Additional metadata
- Larger icons

**Best for**: Browsing applications or when you need more information

### Switching Views

- Click the view toggle button
- Press `Tab` to switch
- Preference is saved between sessions

## Extensions

Launcher supports extensions to add functionality.

### Available Extensions

1. **Application Search**: Default search for installed apps (enabled by default)
2. **Math Calculator**: Built-in calculator (enabled by default)
3. **Command Runner**: Execute shell commands (in development)
4. **AI Assistant**: Natural language queries (in development)
5. **File Manager**: Browse and search files (in development)
6. **Link Management**: Manage web bookmarks (in development)

### Managing Extensions

**Enable/Disable Extensions:**
1. Open Launcher
2. Access Preferences (gear icon or `Ctrl+,`)
3. Navigate to Extensions tab
4. Toggle extensions on/off

**Extension Settings:**
- Each extension may have its own configuration
- Access from the Extensions preferences panel
- Changes take effect immediately

## Preferences

Access preferences through:
- Preferences button in the UI
- Keyboard shortcut `Ctrl+,`
- Main menu → Preferences

### General Settings

- **Startup behavior**: Launch on login
- **Window position**: Remember last position
- **Theme**: Follow system or set custom

### Search Settings

- **Search delay**: Instant vs debounced
- **Result limit**: Maximum results to show
- **Fuzzy matching**: Enable/disable

### Extension Configuration

- Enable/disable specific extensions
- Configure extension-specific settings
- Set extension priorities

### Keyboard Shortcuts

- View current shortcuts
- Customize keyboard bindings
- Reset to defaults

## Tips & Tricks

### Productivity Tips

1. **Pin Favorites**: Keep frequently used apps at the top
2. **Use Keywords**: Create custom keywords for quick access
3. **Learn Math Mode**: Use calculator without switching apps
4. **Keyboard First**: Learn shortcuts for fastest workflow

### Advanced Usage

**Search Tips:**
- Use partial names for faster typing
- Application icons help visual recognition
- Clear search with `Esc` then `Esc` to close

**Performance:**
- Launcher caches desktop entries for fast startup
- Icon caching reduces load times
- Database optimizations for instant search

**Customization:**
- SVG icons scale perfectly at any size
- Preferences are stored in SQLite database
- Extension configurations persist between sessions

### Desktop Integration

**GNOME:**
- Launcher appears in Activities
- Can be pinned to dash/favorites
- Integrates with GNOME Shell search

**Other DEs:**
- Add to application menu
- Create custom keyboard shortcuts
- Use as default launcher

## Common Workflows

### Quick Application Launch
1. Press shortcut to open Launcher
2. Type first few letters
3. Press Enter when highlighted
4. Total time: ~2 seconds

### Calculator
1. Open Launcher
2. Type mathematical expression
3. View result instantly
4. Press Enter to copy result (if supported)

### Browsing Applications
1. Open Launcher with empty search
2. Scroll through all installed apps
3. Switch to extended view for details
4. Click or Enter to launch

## Troubleshooting

**Launcher doesn't show all apps:**
- Check if apps have valid `.desktop` files
- Verify file locations: `/usr/share/applications` and `~/.local/share/applications`

**Search is slow:**
- First launch may be slower (building cache)
- Subsequent launches should be instant

**Icons not showing:**
- Ensure icon themes are installed
- Check GTK4 icon theme settings

For more help, see [FAQ](FAQ.md) or [GitHub Issues](https://github.com/BottyIvan/launcher-app/issues).

## Next Steps

- Explore [Features](Features.md) for detailed capability information
- Read [Configuration](Configuration.md) for advanced customization
- Check [FAQ](FAQ.md) for common questions
