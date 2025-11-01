# Blueprint Quick Reference

Quick reference for common Blueprint patterns used in this project.

## Basic Syntax

```blueprint
using Gtk 4.0;
using Adw 1;

template $ClassName : ParentClass {
  // Properties
  property-name: value;
  
  // Children
  ChildWidget child_id {
    property: value;
  }
}
```

## Common Widgets

### Box (Container)

```blueprint
Box {
  orientation: vertical;  // or horizontal
  spacing: 6;
  margin-top: 12;
  margin-bottom: 12;
  margin-start: 12;
  margin-end: 12;
  
  // Children here
}
```

### Label

```blueprint
Label {
  label: "Hello World";
  xalign: 0;              // 0 = left, 0.5 = center, 1 = right
  wrap: true;
  ellipsize: end;         // none, start, middle, end
  max-width-chars: 50;
}
```

### Button

```blueprint
Button my_button {
  label: "Click Me";
  valign: center;
  tooltip-text: "Button tooltip";
  
  styles ["flat", "pill", "suggested-action", "destructive-action"]
}
```

### Entry (Text Input)

```blueprint
Entry {
  placeholder-text: "Type here...";
  primary-icon-name: "search-symbolic";
  secondary-icon-name: "clear-symbolic";
  
  styles ["flat"]
}
```

### ListBox

```blueprint
ListBox {
  selection-mode: single;  // none, single, multiple
  
  styles ["boxed-list", "boxed-list-separate"]
}
```

### ScrolledWindow

```blueprint
ScrolledWindow {
  vexpand: true;
  hexpand: true;
  hscrollbar-policy: automatic;  // never, automatic, always
  vscrollbar-policy: automatic;
  
  child: ListBox {
    // List content
  }
}
```

## Adwaita Widgets

### ApplicationWindow

```blueprint
using Adw 1;

template $MyWindow : Adw.ApplicationWindow {
  default-width: 600;
  default-height: 400;
  resizable: false;
  
  content: Box {
    // Window content
  }
}
```

### PreferencesDialog

```blueprint
template $MyPrefs : Adw.PreferencesDialog {
  title: "Preferences";
  
  Adw.PreferencesPage {
    title: "General";
    icon-name: "preferences-system-symbolic";
    
    Adw.PreferencesGroup {
      title: "Settings";
      
      Adw.SwitchRow {
        title: "Enable Feature";
        subtitle: "Description here";
      }
    }
  }
}
```

### SwitchRow

```blueprint
Adw.SwitchRow my_switch {
  title: "Enable Feature";
  subtitle: "Optional description";
  active: true;  // Default state
}
```

### ActionRow

```blueprint
Adw.ActionRow {
  title: "Row Title";
  subtitle: "Row subtitle";
  activatable: true;  // Makes it clickable
}
```

### PasswordEntryRow

```blueprint
Adw.PasswordEntryRow api_key_entry {
  title: "API Key";
  show-apply-button: true;
}
```

### ComboRow

```blueprint
Adw.ComboRow {
  title: "Select Option";
  subtitle: "Choose from list";
  model: StringList {
    strings [
      "Option 1",
      "Option 2",
      "Option 3"
    ]
  };
}
```

### ButtonContent

```blueprint
Button {
  Adw.ButtonContent {
    icon-name: "document-save-symbolic";
    label: "Save";
  }
}
```

## Styling

### CSS Classes

```blueprint
Widget {
  styles ["class1", "class2", "class3"]
}
```

Common classes:
- `"flat"` - Flat appearance
- `"pill"` - Rounded pill shape
- `"circular"` - Circular button
- `"suggested-action"` - Blue accent (primary action)
- `"destructive-action"` - Red accent (dangerous action)
- `"dim-label"` - Dimmed text
- `"title-1"`, `"title-2"`, `"title-3"`, `"title-4"` - Title sizes
- `"heading"` - Heading text
- `"caption"` - Small caption text
- `"monospace"` - Monospace font

### Style Block

```blueprint
Widget {
  styles ["class1"]
  
  style {
    // Custom CSS can go here in some cases
  }
}
```

## Layout Properties

### Alignment

```blueprint
Widget {
  valign: start;    // start, center, end, fill
  halign: center;   // start, center, end, fill
}
```

### Expanding

```blueprint
Widget {
  vexpand: true;    // Expand vertically
  hexpand: true;    // Expand horizontally
}
```

### Size

```blueprint
Widget {
  width-request: 400;
  height-request: 300;
}
```

### Margins

```blueprint
Widget {
  margin-top: 6;
  margin-bottom: 6;
  margin-start: 12;
  margin-end: 12;
}
```

## Icon Names

Common symbolic icons:
- `"system-search-symbolic"`
- `"edit-clear-symbolic"`
- `"document-save-symbolic"`
- `"preferences-system-symbolic"`
- `"applications-system-symbolic"`
- `"keyboard-enter-symbolic"`
- `"arrow1-up-symbolic"`
- `"arrow1-down-symbolic"`
- `"network-server-symbolic"`
- `"dialog-warning-symbolic"`
- `"emblem-ok-symbolic"`

## Signals (Connect in Python)

Signals must be connected in Python code:

```python
@Gtk.Template(filename='ui/my_widget.ui')
class MyWidget(Gtk.Box):
    __gtype_name__ = 'MyWidget'
    
    my_button = Gtk.Template.Child()
    
    def __init__(self):
        super().__init__()
        # Connect signals
        self.my_button.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, button):
        print("Button clicked!")
```

## Child IDs

Give widgets IDs to reference them in Python:

```blueprint
Button my_button {  // 'my_button' is the ID
  label: "Click";
}
```

```python
my_button = Gtk.Template.Child()  // Matches the ID
```

## Tips

1. **Use meaningful IDs**: `save_button` not `button1`
2. **Keep it simple**: Complex logic goes in Python
3. **Use symbolic icons**: End icon names with `-symbolic`
4. **Style with classes**: Use standard GTK/Adwaita classes
5. **Test frequently**: Compile and check after changes
6. **Comments**: Use `//` for single-line comments

## Resources

- [Blueprint Syntax](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/reference.html)
- [GTK4 Widgets](https://docs.gtk.org/gtk4/visual_index.html)
- [Adwaita Widgets](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/widget-gallery.html)
- [Icon Names](https://gitlab.gnome.org/GNOME/adwaita-icon-theme/)
