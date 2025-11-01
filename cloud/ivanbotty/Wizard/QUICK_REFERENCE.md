# Blueprint UI Quick Reference

## 📋 Quick Start

### Building the Project
```bash
# Setup build
meson setup builddir

# Compile (includes Blueprint compilation)
meson compile -C builddir

# Install
meson install -C builddir
```

### Running the Wizard
```bash
# Run existing wizard (unchanged)
python3 -m cloud.ivanbotty.Wizard

# Run Blueprint example
python3 -m cloud.ivanbotty.Wizard.app_blueprint_example
```

### Validation
```bash
# Validate Blueprint structure and syntax
python3 cloud/ivanbotty/Wizard/validate_blueprint.py
```

## 📁 File Locations

```
cloud/ivanbotty/Wizard/
├── resources/
│   ├── blueprints/          # Edit these .blp files for UI changes
│   │   ├── wizard-window.blp
│   │   ├── wizard-page.blp
│   │   ├── welcome-page.blp
│   │   └── summary-page.blp
│   ├── ui/                  # Auto-generated, don't edit
│   └── wizard.gresource.xml # GResource definition
├── blueprint_ui.py          # UI loader classes
└── app_blueprint_example.py # Integration example
```

## 🎨 Common Blueprint Patterns

### Basic Page Structure
```blueprint
using Gtk 4.0;
using Adw 1;

template $MyPage : Adw.Clamp {
  maximum-size: 640;
  
  Box {
    orientation: vertical;
    spacing: 24;
    margin-top: 48;
    margin-bottom: 48;
    
    Label title {
      styles ["title-1"]
    }
    
    Button action {
      styles ["suggested-action", "pill"]
    }
  }
}
```

### Translatable Strings
```blueprint
Label {
  label: _("Welcome");  // Marked for translation
}
```

### CSS Classes
```blueprint
Button {
  styles [
    "suggested-action",  // Blue background
    "destructive-action", // Red background
    "pill",              // Rounded corners
    "flat"               // No background
  ]
}
```

### Common Widgets
```blueprint
Adw.StatusPage status {
  icon-name: "system-software-install-symbolic";
  title: _("Title");
  description: _("Description");
}

Adw.PreferencesGroup {
  title: _("Settings");
  
  Adw.ActionRow {
    title: _("Option");
    subtitle: _("Description");
  }
}

Adw.Carousel carousel {
  interactive: true;
  allow-long-swipes: true;
}

Adw.CarouselIndicatorDots {
  carousel: carousel;
}
```

## 🐍 Python Integration

### Load Resources
```python
from cloud.ivanbotty.Wizard.blueprint_ui import load_wizard_resources

# Call at application startup
load_wizard_resources()
```

### Use Window
```python
from cloud.ivanbotty.Wizard.blueprint_ui import WizardWindowBlueprint

window = WizardWindowBlueprint(application=app)
carousel = window.carousel
```

### Create Page
```python
from cloud.ivanbotty.Wizard.blueprint_ui import WizardPageBlueprint

page = WizardPageBlueprint(
    title="Welcome",
    subtitle="Let's get started!",
    button_text="Next",
    callback=on_next_clicked
)

carousel.append(page)
```

### Load UI from Resource
```python
from gi.repository import Gtk

builder = Gtk.Builder.new_from_resource(
    "/cloud/ivanbotty/Wizard/ui/wizard-window.ui"
)
widget = builder.get_object("widget_id")
```

## 🔧 Troubleshooting

### Blueprint compiler not found
```bash
# Install blueprint-compiler
sudo apt install blueprint-compiler  # Debian/Ubuntu
sudo dnf install blueprint-compiler  # Fedora
```

### UI not loading
1. Check resources are installed: `ls /usr/share/launcher-app/Wizard/`
2. Check logs for resource loading errors
3. Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
4. Try the fallback UI (should work automatically)

### Validation fails
```bash
# Re-run validation with verbose output
python3 cloud/ivanbotty/Wizard/validate_blueprint.py
```

### Build errors
```bash
# Clean and rebuild
rm -rf builddir
meson setup builddir
meson compile -C builddir
```

## 📚 Resources

- **Full Documentation**: `cloud/ivanbotty/Wizard/resources/README.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **Blueprint Syntax**: https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/
- **Adwaita Widgets**: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/
- **GNOME HIG**: https://developer.gnome.org/hig/

## 🎯 Design Guidelines

### Spacing
- Page margins: 48px vertical, 32px horizontal
- Element spacing: 24px between major components
- Small gaps: 8-12px

### Layout
- Max content width: 640px (use Adw.Clamp)
- Center-aligned text for pages
- Responsive: tightening-threshold: 400

### Colors
- Use CSS classes, not hardcoded colors
- `suggested-action` for primary actions (blue)
- `destructive-action` for dangerous actions (red)
- `dim-label` for secondary text

### Icons
- Use symbolic icons: `-symbolic` suffix
- Standard icons: `system-software-install-symbolic`, `emblem-ok-symbolic`
- Consistent size: usually 64x64 for page icons

### Buttons
- Primary action: `suggested-action` + `pill`
- Single primary action per page
- Clear, action-oriented labels

## ⚡ Tips

1. **Edit Blueprint, not UI**: Always edit .blp files, never .ui files
2. **Rebuild after changes**: Run `meson compile -C builddir` after editing .blp
3. **Test fallback**: Temporarily disable Blueprint to test fallback UI
4. **Use validation**: Run validation script before committing
5. **Check logs**: Enable logging to debug resource loading issues
6. **Follow patterns**: Use existing .blp files as templates

## 📝 Example Workflow

1. Edit Blueprint file: `vim cloud/ivanbotty/Wizard/resources/blueprints/wizard-page.blp`
2. Rebuild: `meson compile -C builddir`
3. Test: `python3 -m cloud.ivanbotty.Wizard.app_blueprint_example`
4. Validate: `python3 cloud/ivanbotty/Wizard/validate_blueprint.py`
5. Commit changes

---

**Need more help?** See the full documentation in `cloud/ivanbotty/Wizard/resources/README.md`
