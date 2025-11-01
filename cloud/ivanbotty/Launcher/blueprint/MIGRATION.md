# Migration Guide: Blueprint Design Pattern

This guide helps developers migrate existing UI code to use the new blueprint design pattern.

## Quick Start

### 1. Import the Blueprint

```python
from cloud.ivanbotty.Launcher.blueprint import UIBlueprint
```

### 2. Initialize in Your Class

```python
class MyWidget:
    def __init__(self):
        self.ui_blueprint = UIBlueprint()
```

### 3. Replace Manual Widget Creation

**Before:**
```python
button = Gtk.Button()
button.set_label("Click Me")
button.add_css_class("flat")
button.set_tooltip_text("Click this button")
button.connect("clicked", self.on_click)
```

**After:**
```python
button = self.ui_blueprint.components.create_button(
    label="Click Me",
    tooltip="Click this button",
    css_classes=["flat"],
    on_click=self.on_click
)
```

## Common Migration Patterns

### Buttons

**Icon Button - Before:**
```python
btn = Gtk.Button()
btn.add_css_class("flat")
btn_icon = Adw.ButtonContent(icon_name="applications-system-symbolic")
btn.set_child(btn_icon)
btn.set_tooltip_text("Open Settings")
btn.set_focus_on_click(False)
btn.connect("clicked", lambda b: self.open_settings())
```

**Icon Button - After:**
```python
btn = self.ui_blueprint.components.create_icon_button(
    icon_name="applications-system-symbolic",
    tooltip="Open Settings",
    on_click=lambda b: self.open_settings()
)
```

### Labels

**Label - Before:**
```python
label = Gtk.Label(label="Hello World")
label.set_xalign(0)
label.set_wrap(True)
label.add_css_class("bold")
```

**Label - After:**
```python
label = self.ui_blueprint.components.create_label(
    text="Hello World",
    bold=True,
    align_start=True,
    wrap=True
)
```

### Boxes

**Container Box - Before:**
```python
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
box.set_vexpand(True)
box.set_hexpand(True)
box.set_margin_start(16)
box.set_margin_end(16)
```

**Container Box - After:**
```python
box = self.ui_blueprint.components.create_box(
    orientation=Gtk.Orientation.VERTICAL,
    spacing="lg",
    expand=True
)
self.ui_blueprint.style.apply_margins(box)
```

### Icons

**Icon - Before:**
```python
gicon = Gio.ThemedIcon.new("folder-symbolic")
image = Gtk.Image.new_from_gicon(gicon)
image.set_pixel_size(28)
image.add_css_class("icon-dropshadow")
```

**Icon - After:**
```python
image = self.ui_blueprint.components.create_icon(
    icon_name="folder-symbolic",
    size="md",
    css_classes=["icon-dropshadow"]
)
```

### Margins and Spacing

**Margins - Before:**
```python
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

widget.set_margin_top(UI_CONFS[PREFERENCES]["margin_top"])
widget.set_margin_bottom(UI_CONFS[PREFERENCES]["margin_bottom"])
widget.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
widget.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
```

**Margins - After:**
```python
self.ui_blueprint.style.apply_margins(widget)

# Or with custom margins:
self.ui_blueprint.style.apply_margins(widget, {
    'top': 8,
    'bottom': 8,
    'start': 16,
    'end': 16
})
```

## Step-by-Step Migration Process

### 1. Analyze Current Widget

Identify:
- Widget types used (buttons, labels, boxes, etc.)
- Styling patterns (margins, spacing, CSS classes)
- Configuration dependencies (UI_CONFS, PREFERENCES)

### 2. Import Blueprint

Add to your file:
```python
from cloud.ivanbotty.Launcher.blueprint import UIBlueprint
```

### 3. Initialize Blueprint

In `__init__`:
```python
self.ui_blueprint = UIBlueprint()
```

### 4. Replace Widget Creation

Use blueprint factory methods:
- `create_button()` for buttons
- `create_label()` for labels
- `create_box()` for containers
- `create_icon()` for icons
- etc.

### 5. Replace Style Configuration

Use blueprint style methods:
- `apply_margins()` for margins
- `apply_spacing()` for box spacing
- `apply_css_classes()` for CSS classes
- `get_layout()` for layout values

### 6. Remove Config Imports

Remove if no longer needed:
```python
# Can be removed:
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
```

### 7. Test

Verify:
- Widget appears correctly
- Styling is consistent
- Functionality works as before
- No regressions

## Examples

### Footer Widget Migration

**Before (footer.py):**
```python
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

class Footer(Adw.Bin):
    def __init__(self, app):
        super().__init__()
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        
        # Create buttons manually...
        preferences_btn = Gtk.Button()
        preferences_btn.add_css_class("flat")
        # ... more configuration
```

**After (using UIBlueprint):**
```python
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Adw
from cloud.ivanbotty.Launcher.blueprint import UIBlueprint

class Footer(Adw.Bin):
    def __init__(self, app):
        super().__init__()
        self.ui_blueprint = UIBlueprint()
        
        main_box = self.ui_blueprint.components.create_box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing="lg"
        )
        self.ui_blueprint.style.apply_margins(self)
        
        # Use blueprint to create buttons
        preferences_btn = self.ui_blueprint.components.create_icon_button(
            icon_name="applications-system-symbolic",
            tooltip="Open Preferences",
            on_click=lambda b: self.open_preferences()
        )
```

### Row Widget Migration

See `cloud/ivanbotty/Launcher/widget/row.py` for a complete example of:
- Blueprint initialization
- Component creation with factory methods
- Style application
- Tag button creation

## Benefits After Migration

1. **Less code**: Factory methods reduce boilerplate
2. **More readable**: Intent is clearer
3. **Consistent styling**: Automatic adherence to design system
4. **Easier maintenance**: Changes in one place affect all components
5. **Better testing**: Mocked blueprints for unit tests

## Backward Compatibility

The blueprint pattern is designed to coexist with existing code:

- Old widgets continue to work
- Gradual migration is supported
- No breaking changes to existing APIs

You can mix old and new patterns during transition:

```python
# Old style still works
old_button = Gtk.Button(label="Old")

# New style
new_button = self.ui_blueprint.components.create_button(label="New")

# Both can exist in the same container
box.append(old_button)
box.append(new_button)
```

## Troubleshooting

### Import Errors

**Problem:** `ImportError: cannot import name 'UIBlueprint'`

**Solution:** Ensure the blueprint package is in your Python path:
```python
import sys
sys.path.insert(0, '/path/to/launcher-app')
```

### GTK Not Available

**Problem:** `ValueError: Namespace Gtk not available`

**Solution:** This is expected in non-GUI environments. The blueprint requires GTK4 to be installed and available.

### Layout Issues

**Problem:** Widget appears with wrong size or margins

**Solution:** Check which layout is active:
```python
print(self.ui_blueprint.style.current_style)
print(self.ui_blueprint.style.get_layout())
```

### Style Not Applied

**Problem:** CSS classes not appearing on widget

**Solution:** Ensure you're using `apply_css_classes`:
```python
# Correct:
self.ui_blueprint.style.apply_css_classes(widget, ["flat", "round"])

# Not recommended:
widget.add_css_class("flat")  # Old way
```

## Next Steps

1. Start with small widgets (buttons, labels)
2. Move to containers (boxes, scrolled windows)
3. Migrate complete layouts
4. Update documentation
5. Remove unused imports

## Resources

- Blueprint README: `cloud/ivanbotty/Launcher/blueprint/README.md`
- Example implementations:
  - `cloud/ivanbotty/Launcher/app.py`
  - `cloud/ivanbotty/Launcher/widget/row.py`
  - `cloud/ivanbotty/Launcher/widget/search_entry.py`

## Questions?

Refer to the main Blueprint README or check the source code for examples of how components are created and styled.
