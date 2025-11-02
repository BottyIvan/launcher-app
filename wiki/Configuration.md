# Configuration

Learn how to configure and customize Launcher to match your preferences.

## Table of Contents

- [Configuration Overview](#configuration-overview)
- [User Preferences](#user-preferences)
- [Extension Configuration](#extension-configuration)
- [Environment Variables](#environment-variables)
- [Configuration Files](#configuration-files)
- [Advanced Configuration](#advanced-configuration)

## Configuration Overview

Launcher stores configuration in multiple locations:

- **User Preferences**: SQLite database (`~/.local/share/cloud.ivanbotty.Launcher/`)
- **Extension Config**: YAML files in resources directory
- **Runtime Settings**: Environment variables
- **System Integration**: Desktop files and GSettings

## User Preferences

### Accessing Preferences

1. **Via UI**: Click the preferences/settings icon in Launcher
2. **Keyboard Shortcut**: Press `Ctrl+,`
3. **From Menu**: Main menu → Preferences

### General Settings

#### Application Behavior

```yaml
# These settings are stored in SQLite database

startup_behavior:
  launch_on_login: false        # Auto-start with desktop session
  show_wizard_on_first_run: true  # Show welcome wizard
  minimize_to_tray: false       # Minimize to system tray

window_settings:
  remember_position: true       # Remember window position
  remember_size: true           # Remember window size
  default_width: 600            # Default window width (pixels)
  default_height: 400           # Default window height (pixels)
  always_on_top: false          # Keep window on top

theme_settings:
  follow_system_theme: true     # Use system theme
  prefer_dark_mode: false       # Force dark mode (if not following system)
```

#### Search Behavior

```yaml
search_settings:
  instant_search: true          # Search as you type (no delay)
  search_delay_ms: 0            # Delay before search triggers (ms)
  max_results: 50               # Maximum results to display
  fuzzy_matching: true          # Enable fuzzy search
  case_sensitive: false         # Case-sensitive search
  search_descriptions: true     # Search in app descriptions (slower)

results_display:
  show_icons: true              # Display application icons
  icon_size: 64                 # Icon size in pixels
  show_descriptions: true       # Show app descriptions (extended mode)
  highlight_matches: true       # Highlight search matches
```

### View Preferences

#### Compact Mode

```yaml
compact_mode:
  grid_columns: 4               # Number of columns
  item_spacing: 10              # Spacing between items (pixels)
  show_labels: true             # Show application names
  icon_size: 48                 # Icon size for compact mode
```

#### Extended Mode

```yaml
extended_mode:
  show_descriptions: true       # Show full descriptions
  show_categories: true         # Display app categories
  show_metadata: true           # Show additional metadata
  icon_size: 64                 # Icon size for extended mode
  row_height: 80                # Height of each row (pixels)
```

### Keyboard Shortcuts

```yaml
keyboard_shortcuts:
  # Global shortcuts (system-wide)
  toggle_launcher: "Super+Space"    # Open/close Launcher
  
  # Application shortcuts (when Launcher is open)
  navigate_up: "Up"                 # Move selection up
  navigate_down: "Down"             # Move selection down
  activate: "Return"                # Launch selected app
  close_window: "Escape"            # Close Launcher
  toggle_view: "Tab"                # Switch compact/extended
  preferences: "Ctrl+comma"         # Open preferences
  refresh: "F5"                     # Refresh application list
  
  # Search shortcuts
  select_all: "Ctrl+a"              # Select all search text
  copy: "Ctrl+c"                    # Copy selected text
  paste: "Ctrl+v"                   # Paste text
  clear_search: "Ctrl+u"            # Clear search field
```

## Extension Configuration

### Managing Extensions

Access extension settings through:
- Preferences → Extensions tab
- Extensions configuration file

### Extension Settings File

Location: `cloud/ivanbotty/Launcher/resources/extensions.yaml`

```yaml
extensions:
  - name: "Application Search"
    id: "app_search"
    enabled: true
    priority: 1
    description: "Search and launch installed applications"
    handler: "cloud.ivanbotty.Launcher.handlers.applications_handler.ApplicationsHandler"
    service: "cloud.ivanbotty.Launcher.services.applications_service.ApplicationsService"
    icon: "system-search"
    settings:
      search_paths:
        - "/usr/share/applications"
        - "~/.local/share/applications"
      cache_duration: 3600  # seconds

  - name: "Math Calculator"
    id: "math_calc"
    enabled: true
    priority: 2
    description: "Evaluate mathematical expressions"
    handler: "cloud.ivanbotty.Launcher.handlers.math_handler.MathHandler"
    service: "cloud.ivanbotty.Launcher.services.math_service.MathService"
    icon: "accessories-calculator"
    settings:
      decimal_places: 2
      angle_mode: "radians"  # radians or degrees
      
  - name: "Command Runner"
    id: "command"
    enabled: false
    priority: 3
    description: "Execute shell commands"
    handler: "cloud.ivanbotty.Launcher.handlers.command_handler.CommandHandler"
    service: "cloud.ivanbotty.Launcher.services.command_service.CommandService"
    icon: "utilities-terminal"
    settings:
      allowed_commands: []  # Empty = allow all (use with caution)
      history_size: 100
      show_output: true

  - name: "AI Assistant"
    id: "ai_assistant"
    enabled: false
    priority: 4
    description: "AI-powered natural language queries"
    handler: "cloud.ivanbotty.Launcher.handlers.ai_handler.AIHandler"
    service: "cloud.ivanbotty.Launcher.services.ai_service.AIService"
    icon: "dialog-question"
    settings:
      api_provider: "gemini"
      model: "gemini-pro"
      api_key: ""  # Set via environment variable
      temperature: 0.7
      max_tokens: 150
```

### Per-Extension Configuration

#### Application Search Extension

```yaml
app_search_settings:
  # Desktop file locations
  search_paths:
    - "/usr/share/applications"
    - "/usr/local/share/applications"
    - "~/.local/share/applications"
    - "/var/lib/flatpak/exports/share/applications"
    - "~/.local/share/flatpak/exports/share/applications"
  
  # Cache settings
  cache_enabled: true
  cache_duration: 3600  # seconds (1 hour)
  auto_refresh: true
  
  # Filtering
  show_hidden: false          # Show NoDisplay=true apps
  show_terminal_only: true    # Show Terminal=true apps
  category_filter: []         # Empty = all categories
  
  # Icon settings
  fallback_icon: "application-x-executable"
  icon_theme: "Adwaita"  # null = use system default
```

#### Math Calculator Extension

```yaml
math_settings:
  # Display settings
  decimal_places: 2
  scientific_notation: false
  thousands_separator: false
  
  # Calculation settings
  angle_mode: "radians"  # radians or degrees
  precision: 15          # Internal precision
  
  # Allowed functions
  functions:
    - sqrt, pow, exp, log, log10
    - sin, cos, tan, asin, acos, atan
    - sinh, cosh, tanh
    - abs, ceil, floor, round
  
  # Constants
  constants:
    pi: 3.141592653589793
    e: 2.718281828459045
    phi: 1.618033988749895  # Golden ratio
```

#### AI Assistant Extension

```yaml
ai_settings:
  # API Configuration
  provider: "gemini"
  model: "gemini-pro"
  api_key_env: "GEMINI_API_KEY"  # Environment variable name
  endpoint: "https://generativelanguage.googleapis.com/v1beta"
  
  # Generation settings
  temperature: 0.7       # 0.0-1.0 (creativity)
  max_tokens: 150        # Maximum response length
  top_p: 0.9            # Nucleus sampling
  top_k: 40             # Top-k sampling
  
  # Behavior
  streaming: false       # Stream responses
  context_length: 5      # Number of previous messages
  system_prompt: "You are a helpful assistant integrated into a Linux application launcher."
  
  # Safety
  safety_settings:
    harassment: "BLOCK_MEDIUM_AND_ABOVE"
    hate_speech: "BLOCK_MEDIUM_AND_ABOVE"
    sexually_explicit: "BLOCK_MEDIUM_AND_ABOVE"
    dangerous_content: "BLOCK_MEDIUM_AND_ABOVE"
```

## Environment Variables

Override default settings using environment variables:

### Application Settings

```bash
# Data directories
export LAUNCHER_DATA_DIR="$HOME/.local/share/cloud.ivanbotty.Launcher"
export LAUNCHER_CONFIG_DIR="$HOME/.config/cloud.ivanbotty.Launcher"
export LAUNCHER_CACHE_DIR="$HOME/.cache/cloud.ivanbotty.Launcher"

# Logging
export LAUNCHER_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
export LAUNCHER_LOG_FILE="$HOME/.local/share/cloud.ivanbotty.Launcher/launcher.log"

# Performance
export LAUNCHER_CACHE_ENABLED="1"
export LAUNCHER_THREAD_POOL_SIZE="4"

# Debug mode
export LAUNCHER_DEBUG="0"  # 1 to enable debug mode
```

### Extension Settings

```bash
# AI Service
export GEMINI_API_KEY="your-api-key-here"
export AI_MODEL="gemini-pro"
export AI_TEMPERATURE="0.7"

# Command Service
export LAUNCHER_ALLOW_COMMANDS="1"  # 1 to allow command execution
export LAUNCHER_COMMAND_TIMEOUT="30"  # seconds
```

### GTK/Display Settings

```bash
# GTK theme
export GTK_THEME="Adwaita:dark"

# Display scaling
export GDK_SCALE="2"  # HiDPI scaling factor
export GDK_DPI_SCALE="0.5"

# Wayland/X11
export GDK_BACKEND="wayland"  # wayland or x11
```

## Configuration Files

### Database Schema

User preferences are stored in SQLite database:

```sql
-- Location: ~/.local/share/cloud.ivanbotty.Launcher/launcher.db

-- Preferences table
CREATE TABLE preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    type TEXT NOT NULL,  -- string, int, bool, json
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Extensions state
CREATE TABLE extension_state (
    extension_id TEXT PRIMARY KEY,
    enabled BOOLEAN DEFAULT 1,
    priority INTEGER,
    settings TEXT  -- JSON
);

-- Application cache (optional)
CREATE TABLE app_cache (
    desktop_id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    icon TEXT,
    exec TEXT,
    categories TEXT,
    cached_at TIMESTAMP
);
```

### Resource Files

```
cloud/ivanbotty/Launcher/resources/
├── extensions.yaml          # Extension definitions
├── wizard.yaml              # Welcome wizard config
├── resources.xml            # GResource bundle
├── appdata.xml              # AppStream metadata
└── *.svg                    # Icon files
```

## Advanced Configuration

### Custom Application Paths

Add custom desktop file locations:

```python
# In your local extensions.yaml or via preferences
app_search_settings:
  additional_paths:
    - "/opt/applications"
    - "$HOME/custom-apps"
```

### Custom Icon Themes

```bash
# Set custom icon theme
gsettings set org.gnome.desktop.interface icon-theme 'Papirus'

# Or via environment
export GTK_ICON_THEME="Papirus"
```

### Performance Tuning

```yaml
performance:
  # Database
  db_cache_size: 10000        # SQLite cache size (KB)
  db_synchronous: "NORMAL"    # OFF, NORMAL, FULL
  
  # Threading
  thread_pool_size: 4         # Background worker threads
  async_search: true          # Non-blocking search
  
  # Caching
  icon_cache_size: 100        # Cached icon paths
  app_cache_size: 500         # Cached app entries
  cache_ttl: 3600             # Cache TTL (seconds)
```

### Debug Configuration

Enable detailed logging:

```bash
# Run with debug output
LAUNCHER_LOG_LEVEL=DEBUG flatpak run cloud.ivanbotty.Launcher

# Or with Python
LAUNCHER_LOG_LEVEL=DEBUG python3 -m cloud.ivanbotty.Launcher
```

Debug configuration:

```yaml
debug:
  log_level: "DEBUG"
  log_to_file: true
  log_file: "~/.local/share/cloud.ivanbotty.Launcher/debug.log"
  log_format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
  # Performance profiling
  profile_enabled: false
  profile_output: "/tmp/launcher-profile.prof"
  
  # GTK Inspector
  enable_inspector: true  # GTK_DEBUG=interactive
```

### Flatpak-Specific Configuration

When running as Flatpak, some paths are different:

```bash
# Data directory
~/.var/app/cloud.ivanbotty.Launcher/data/cloud.ivanbotty.Launcher/

# Config directory
~/.var/app/cloud.ivanbotty.Launcher/config/cloud.ivanbotty.Launcher/

# Access host files (read-only)
/run/host/  # Host filesystem

# Override Flatpak settings
flatpak override --user cloud.ivanbotty.Launcher --filesystem=home
```

## Configuration Examples

### Minimal Configuration

For a clean, minimal setup:

```yaml
general:
  show_icons: true
  max_results: 20
  
extensions:
  enabled:
    - app_search
```

### Power User Configuration

For advanced users:

```yaml
general:
  instant_search: true
  fuzzy_matching: true
  max_results: 100
  show_descriptions: true

keyboard_shortcuts:
  toggle_launcher: "Super+Space"
  quick_calc: "Super+C"

extensions:
  enabled:
    - app_search
    - math_calc
    - command
    - ai_assistant

performance:
  thread_pool_size: 8
  cache_size: 1000
```

### Developer Configuration

For development and testing:

```yaml
debug:
  log_level: "DEBUG"
  enable_inspector: true
  profile_enabled: true

development:
  reload_on_change: true
  show_widget_bounds: true
  verbose_errors: true
```

## Resetting Configuration

### Reset to Defaults

```bash
# Remove database (will be recreated)
rm ~/.local/share/cloud.ivanbotty.Launcher/launcher.db

# Or for Flatpak
rm ~/.var/app/cloud.ivanbotty.Launcher/data/cloud.ivanbotty.Launcher/launcher.db
```

### Backup Configuration

```bash
# Backup user data
cp -r ~/.local/share/cloud.ivanbotty.Launcher ~/launcher-backup

# Restore from backup
cp -r ~/launcher-backup/* ~/.local/share/cloud.ivanbotty.Launcher/
```

## Next Steps

- Read the [Usage Guide](Usage-Guide.md) to learn how to use configured features
- Check [FAQ](FAQ.md) for configuration troubleshooting
- See [Architecture](Architecture.md) for technical details
