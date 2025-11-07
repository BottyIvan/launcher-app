# UI Enhancement Visual Reference

Visual description of the UI enhancements using native Adwaita styling.

## Main Window

### Search Entry
```
┌─────────────────────────────────────────────────────────────┐
│  🔍  Type to search...                                   ✕  │
└─────────────────────────────────────────────────────────────┘
    ↑                                                        ↑
  Search icon                              Clear (dynamic, appears on input)
```

**Native Styling:**
- `.flat` class for borderless style
- Dynamic clear button
- Height: 52px (default), 40px (compact)

### Results List

```
┌─────────────────────────────────────────────────────────────┐
│  [Icon]  Application Name                        [APP]      │
│          Brief description                                   │
├─────────────────────────────────────────────────────────────┤
│  [Icon]  Calculator                             [MATH]      │
│          Quick calculations                                  │
└─────────────────────────────────────────────────────────────┘
```

**Native Classes:**
- `.heading` - App names (bold)
- `.dim-label` - Descriptions (dimmed)
- `.pill` + `.accent`/`.success`/`.warning` - Category tags
- Icon size: 32px (configurable)

### Footer

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙                         ↑↓ Navigate  ↵ Select  Esc Close │
└─────────────────────────────────────────────────────────────┘
    ↑                                    ↑
  Preferences (.circular)           Labels (.dim-label, .caption)
```

## Category Tags

Tags use native Adwaita style classes:

- **Application** → `.accent` (system accent color)
- **Math** → `.success` (green)
- **AI** → `.accent` (purple/blue)
- **Command** → `.warning` (orange)
- **File** → `.accent` (default)

All styled with `.pill` for pill shape.

## Native Adwaita Classes

### Text Styles
- `.heading` - Bold, larger text
- `.dim-label` - 55% opacity
- `.caption` - Smaller font size
- `.monospace` - Code snippets

### Button Styles
- `.flat` - No background
- `.circular` - Circular button
- `.pill` - Pill-shaped button

### Color Classes
- `.accent` - System accent color (blue by default)
- `.success` - Green tone
- `.warning` - Orange tone
- `.error` - Red tone

## Layout Modes

### Default (850x580)
- Full spacing: 20px horizontal, 16px vertical
- Entry: 810x52
- Icon: 32px

### Compact (700x400)
- Reduced spacing: 10px all around
- Entry: 660x40
- Icon: 32px

### Minimum (600x400)
- Window constraints enforce this minimum

## Configuration

All settings in `config.py`:

```python
# Icon sizes
UI_CONFS[style]["icon_size"] = 32

# Tag colors
CATEGORY_TAG_STYLES = {
    "application": "accent",
    "math": "success",
}

# Animations
ANIMATION_SETTINGS = {
    "enable_animations": True,
    "transition_duration": 200,
}
```

## Theme Compatibility

### Light Theme
- Text: System foreground
- Background: System background
- Accent: System accent (typically blue)

### Dark Theme
- Automatic adaptation
- No custom colors needed
- Uses Adwaita dark palette

### High Contrast
- Automatically supported
- No modifications needed
- Native GTK handling

## Keyboard Shortcuts

Accessible via Ctrl+? or F1:

**Navigation**
- Type → Search
- ↑/↓ → Navigate
- Enter → Launch
- Escape → Close
- Backspace → Clear

**Application**
- Ctrl+, → Preferences
- Ctrl+Q → Quit
- Ctrl+?/F1 → Help

## Implementation Notes

- No custom CSS files
- All styling via Adwaita classes
- Configurable via `config.py`
- Theme-agnostic
- Accessibility-first
