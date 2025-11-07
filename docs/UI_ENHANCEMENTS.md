# Launcher App - UI Enhancement Documentation

This document describes the modern UI improvements made to the Launcher application following GNOME Human Interface Guidelines (HIG), using native Adwaita styling and code-based configuration.

## Overview

The Launcher app UI has been enhanced to provide a more professional, modern, and productivity-focused experience while maintaining performance, simplicity, and full compatibility with system themes.

### Design Philosophy

**Native Adwaita First** - All styling uses native Adwaita CSS classes instead of custom stylesheets to ensure:
- Compatibility with system themes
- Respect for user accessibility preferences
- Automatic dark/light mode support
- No maintenance burden for custom CSS

**Configuration-Based** - Visual parameters are defined in code (`config.py`) for easy customization without touching source files.

## Key Improvements

### 1. Enhanced Search Entry

**File:** `cloud/ivanbotty/Launcher/widget/search_entry.py`

- Dynamic clear button (only shows when text is entered)
- Native `.flat` styling
- Keyboard accessible

### 2. Native Category Tags

**File:** `cloud/ivanbotty/Launcher/widget/row.py`

- Uses native Adwaita classes: `.pill`, `.accent`, `.success`, `.warning`
- Configurable icon sizes from `UI_CONFS`
- Better text hierarchy with `.heading` and `.dim-label`

**Tag Styling (config.py):**
```python
CATEGORY_TAG_STYLES = {
    "application": "accent",   # System accent color
    "math": "success",         # Green
    "ai": "accent",            # Purple/blue
    "command": "warning",      # Orange
}
```

### 3. Keyboard Shortcuts Overlay

**File:** `cloud/ivanbotty/Launcher/widget/window.py`

- Native `Gtk.ShortcutsWindow`
- Accessible via `Ctrl+?` or `F1`
- Shows all available shortcuts

### 4. Organized Preferences

**File:** `cloud/ivanbotty/Launcher/widget/preferences.py`

- 4 pages: General, Appearance, Extensions, API Keys
- Native `Adw.PreferencesDialog`
- Modern Adwaita widgets

## Configuration System

### Layout Settings (config.py)

```python
UI_CONFS = {
    "compact": {
        "width": 700,
        "height": 400,
        "icon_size": 32,
        # ...
    },
    "default": {
        "width": 850,
        "height": 580,
        "icon_size": 32,
        # ...
    },
}
```

### Animation Settings

```python
ANIMATION_SETTINGS = {
    "enable_animations": True,
    "transition_duration": 200,  # milliseconds
}
```

## Adwaita Classes Used

### Typography
- `.heading` - App names
- `.dim-label` - Secondary text
- `.caption` - Small text
- `.monospace` - Code

### Buttons
- `.flat` - No background
- `.circular` - Round shape
- `.pill` - Pill shape

### Colors
- `.accent` - System accent
- `.success` - Green
- `.warning` - Orange
- `.error` - Red

## Benefits

### Theme Compatibility
- Works with all GTK themes
- Automatic dark/light mode
- Consistent with GNOME apps

### Accessibility
- Respects font sizes
- High contrast support
- Screen reader compatible
- Honors "Reduce motion"

### Maintainability
- No custom CSS
- Auto-updates with GTK
- Less code to maintain

## Testing

### Visual
1. Test different themes
2. Check dark/light modes
3. Verify high contrast

### Accessibility
1. Large text setting
2. Screen reader
3. Keyboard only
4. Reduce motion

## References

- [GNOME HIG](https://developer.gnome.org/hig/)
- [Adwaita Style Classes](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/style-classes.html)
- [GTK4 Docs](https://docs.gtk.org/gtk4/)
