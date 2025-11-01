# GTK Blueprint Migration Guide

This guide explains how to migrate existing GTK widgets to use Blueprint templates.

## Overview

GTK Blueprint provides a declarative way to define UI layouts, separating UI structure from business logic. This makes the code more maintainable and easier to understand.

## Migration Steps

### Step 1: Create a Blueprint File

Create a `.blp` file in the `ui/` directory that describes your widget's structure.

**Example: Before (Python only)**
```python
class MyWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        label = Gtk.Label(label="Hello")
        self.append(label)
        
        button = Gtk.Button(label="Click Me")
        button.connect("clicked", self.on_button_clicked)
        self.append(button)
```

**After (Blueprint + Python)**

Create `ui/my_widget.blp`:
```blueprint
using Gtk 4.0;

template $MyWidget : Gtk.Box {
  orientation: vertical;
  spacing: 6;
  
  Label {
    label: "Hello";
  }
  
  Button my_button {
    label: "Click Me";
  }
}
```

### Step 2: Compile the Blueprint

```bash
python3 compile_blueprints.py
# or
blueprint-compiler compile --output ui/my_widget.ui ui/my_widget.blp
```

### Step 3: Update the Python Class

```python
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'my_widget.ui'))
class MyWidget(Gtk.Box):
    __gtype_name__ = 'MyWidget'  # Must match the template name
    
    # Bind template children by ID
    my_button = Gtk.Template.Child()
    
    def __init__(self):
        super().__init__()
        # Connect signals
        self.my_button.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, button):
        print("Button clicked!")
```

## Key Concepts

### 1. Template Decorator

The `@Gtk.Template()` decorator tells GTK to load the UI from a file:

```python
@Gtk.Template(filename='path/to/file.ui')
class MyWidget(Gtk.SomeWidget):
    __gtype_name__ = 'MyWidget'  # Must match template class name
```

### 2. Template Children

Use `Gtk.Template.Child()` to bind widgets defined in the UI file:

```python
# In Blueprint (.blp):
# Button my_button { ... }

# In Python:
my_button = Gtk.Template.Child()  # Matches the ID 'my_button'
```

### 3. GType Name

The `__gtype_name__` must match the template name in the Blueprint file:

```blueprint
template $MyWidget : Gtk.Box { }  # Template name is MyWidget
```

```python
class MyWidget(Gtk.Box):
    __gtype_name__ = 'MyWidget'  # Must match
```

## Common Patterns

### Pattern 1: Simple Widget

**Blueprint:**
```blueprint
using Gtk 4.0;

template $SearchEntry : Gtk.Entry {
  placeholder-text: "Type to search...";
  primary-icon-name: "system-search-symbolic";
}
```

**Python:**
```python
@Gtk.Template(filename='ui/search_entry.ui')
class SearchEntry(Gtk.Entry):
    __gtype_name__ = 'SearchEntry'
    
    def __init__(self):
        super().__init__()
```

### Pattern 2: Widget with Children

**Blueprint:**
```blueprint
using Gtk 4.0;

template $MyBox : Gtk.Box {
  orientation: vertical;
  
  Label title_label {
    label: "Title";
  }
  
  Entry text_entry { }
}
```

**Python:**
```python
@Gtk.Template(filename='ui/my_box.ui')
class MyBox(Gtk.Box):
    __gtype_name__ = 'MyBox'
    
    title_label = Gtk.Template.Child()
    text_entry = Gtk.Template.Child()
    
    def __init__(self):
        super().__init__()
        # Access children
        self.title_label.set_text("New Title")
```

### Pattern 3: Adwaita Widgets

**Blueprint:**
```blueprint
using Gtk 4.0;
using Adw 1;

template $MyPreferences : Adw.PreferencesDialog {
  title: "Settings";
  
  Adw.PreferencesPage {
    Adw.PreferencesGroup {
      title: "General";
      
      Adw.SwitchRow my_switch {
        title: "Enable Feature";
      }
    }
  }
}
```

**Python:**
```python
@Gtk.Template(filename='ui/my_preferences.ui')
class MyPreferences(Adw.PreferencesDialog):
    __gtype_name__ = 'MyPreferences'
    
    my_switch = Gtk.Template.Child()
    
    def __init__(self):
        super().__init__()
        self.my_switch.connect("notify::active", self.on_switch_toggled)
```

## Migration Checklist for Existing Widgets

For each widget you want to migrate:

- [ ] Create a `.blp` file with the widget's UI structure
- [ ] Define all child widgets with unique IDs
- [ ] Compile the Blueprint to `.ui` format
- [ ] Add `@Gtk.Template()` decorator to the Python class
- [ ] Set `__gtype_name__` to match the template name
- [ ] Replace widget creation code with `Gtk.Template.Child()` bindings
- [ ] Keep signal connections and business logic in Python
- [ ] Test the widget to ensure it works correctly

## Benefits of Using Blueprint

1. **Separation of Concerns**: UI structure is separate from business logic
2. **Declarative Syntax**: More readable than imperative Python code
3. **IDE Support**: Many editors have Blueprint syntax highlighting
4. **GTK Best Practices**: Blueprint encourages proper GTK patterns
5. **Easier Maintenance**: UI changes don't require code recompilation
6. **Visual Tools**: Can use GTK Inspector to view and debug templates

## Tips and Best Practices

1. **Start Small**: Migrate simple widgets first to learn the pattern
2. **Keep Logic in Python**: Only UI structure goes in Blueprint
3. **Use Meaningful IDs**: Name template children clearly (e.g., `save_button`, not `button1`)
4. **Test Frequently**: Compile and test after each change
5. **Version Control**: Commit both `.blp` and `.ui` files
6. **Document Custom Widgets**: Add comments in Blueprint for complex layouts

## Resources

- [Blueprint Tutorial](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/tutorial.html)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Libadwaita Documentation](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/)
- See `examples_blueprint.py` in this repository for working examples

## Troubleshooting

### Error: "Template class not found"

Make sure `__gtype_name__` in Python matches the template name in Blueprint.

### Error: "Child widget not found"

Ensure the child ID in Blueprint matches the variable name in Python exactly.

### UI Not Loading

Check that the `.ui` file is compiled and the path in `@Gtk.Template(filename=...)` is correct.

### Changes Not Appearing

Recompile the Blueprint file after making changes:
```bash
python3 compile_blueprints.py
```
