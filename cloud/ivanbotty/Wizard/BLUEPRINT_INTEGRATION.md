# Blueprint UI Integration - Wizard Module

This document describes the GNOME Blueprint UI implementation for the Wizard module in the Launcher App.

## Overview

The Wizard module now uses **GNOME Blueprint** to define its user interface declaratively. Blueprint files (`.blp`) are compiled to GTK UI files (`.ui`) at build time using `blueprint-compiler`, then bundled into GResource files for runtime loading.

## Architecture

### Directory Structure

```
cloud/ivanbotty/Wizard/
├── __main__.py              # Entry point with resource loading
├── app.py                   # Original wizard app (legacy)
├── blueprint_app.py         # Blueprint-based wizard app
├── components/
│   ├── page.py             # Original page component (legacy)
│   └── blueprint_pages.py  # Blueprint page templates (legacy, kept for reference)
└── resources/
    ├── blueprints/         # Source Blueprint files
    │   ├── wizard-window.blp
    │   ├── welcome-page.blp
    │   └── summary-page.blp
    └── resources.xml       # GResource manifest
```

### Blueprint Files

1. **wizard-window.blp** - Main application window with:
   - `AdwApplicationWindow` as the root
   - `AdwHeaderBar` with title
   - `AdwCarousel` for page navigation
   - `AdwCarouselIndicatorDots` for visual navigation

2. **welcome-page.blp** - Welcome/first page with:
   - Centered content using `AdwClamp`
   - Title and subtitle labels
   - "Next" action button

3. **summary-page.blp** - Final summary page with:
   - Similar layout to welcome page
   - "Finish" action button

### Build Process

The Meson build system handles Blueprint compilation:

1. **Blueprint Compilation** (`meson.build`):
   - Uses `blueprint-compiler batch-compile` to convert `.blp` → `.ui`
   - Runs as a custom target during build
   - Output: `.ui` files in the build directory

2. **Resource Bundling**:
   - `gnome.compile_resources()` bundles `.ui` files into `wizard-resources.gresource`
   - Resources are prefixed with `/cloud/ivanbotty/Wizard/`
   - Installed to `<datadir>/launcher-app/Wizard/`

3. **Python Integration**:
   - `__main__.py` loads the `.gresource` file at startup
   - Template classes are initialized after resource registration
   - UI components use `@Gtk.Template()` decorator to bind to Blueprint UI

## Key Features

- **Declarative UI**: Layout defined in Blueprint, not Python code
- **Build-time compilation**: Blueprint → UI conversion happens during build
- **Resource embedding**: UI files bundled for efficient distribution
- **Type safety**: Template Child bindings provide compile-time checks
- **Maintainability**: Separate UI definition from business logic
- **Adwaita styling**: Native GNOME design patterns and widgets

## Usage

### Building the Project

```bash
meson setup build
meson compile -C build
```

Requirements:
- `blueprint-compiler` (0.12.0+)
- `libgtk-4-dev`
- `libadwaita-1-dev`
- `libglib2.0-dev`

### Running the Wizard

```bash
# From repository root
python3 -m cloud.ivanbotty.Wizard

# Or after installation
cloud-ivanbotty-wizard
```

### Modifying the UI

1. Edit the appropriate `.blp` file in `resources/blueprints/`
2. Rebuild the project with `meson compile -C build`
3. The changes will be reflected in the next run

## Technical Details

### Resource Loading Order

Critical: Resources must be loaded **before** importing template classes:

```python
# 1. Load GResource file
resource = Gio.Resource.load(resource_path)
Gio.resources_register(resource)

# 2. Import app with templates
from cloud.ivanbotty.Wizard.blueprint_app import WelcomeWizard

# 3. Initialize and run app
app = WelcomeWizard(...)
app.run()
```

### Template Class Pattern

Template classes use lazy initialization:

```python
# Template is validated when decorator is applied
@Gtk.Template(resource_path="/cloud/ivanbotty/Wizard/wizard-window.ui")
class WizardWindow(Adw.ApplicationWindow):
    __gtype_name__ = "WizardWindow"
    
    # Bind UI elements using Template.Child()
    content_carousel = Gtk.Template.Child()
    window_title = Gtk.Template.Child()
```

### Blueprint Syntax Highlights

- `using Gtk 4.0; using Adw 1;` - Import required libraries
- `template $ClassName : ParentClass { }` - Define template class
- `Widget_id { }` - Create widget with ID for binding
- `_("Text")` - Mark strings as translatable
- `styles [ "class-name" ]` - Apply CSS classes

## Migration from Legacy UI

The original `app.py` creates UI programmatically. The Blueprint version:

- **Before**: Manual widget creation in Python
- **After**: Declarative Blueprint definition + minimal Python glue

Benefits:
- Less Python code to maintain
- UI changes don't require Python changes
- Better separation of concerns
- Easier for designers to contribute
- Standard GNOME tooling support

## Future Enhancements

Potential improvements:

1. Add more wizard pages dynamically from configuration
2. Implement custom widgets in Blueprint
3. Add animations and transitions in Blueprint
4. Use Blueprint for Launcher main UI
5. Add localization/translation support
6. Create reusable Blueprint components library

## References

- [Blueprint Documentation](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Libadwaita Documentation](https://gnome.pages.gitlab.gnome.org/libadwaita/)
- [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/)
