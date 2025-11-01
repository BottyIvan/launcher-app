# GNOME Blueprint UI for Wizard Module

This directory contains the GNOME Blueprint UI implementation for the Launcher App Wizard module.

## Overview

The Wizard module now supports modern GNOME Blueprint UI files (`.blp`), which are compiled to GTK UI files (`.ui`) during the build process and loaded at runtime using GtkBuilder and GResource.

## Directory Structure

```
cloud/ivanbotty/Wizard/
├── app.py                          # Original wizard application
├── app_blueprint_example.py        # Example Blueprint integration
├── blueprint_ui.py                 # Blueprint UI loader classes
├── __main__.py                     # Application entry point
├── components/
│   └── page.py                     # Original page component
├── resources/
│   ├── blueprints/                 # Blueprint source files
│   │   ├── wizard-window.blp       # Main window template
│   │   ├── welcome-page.blp        # Welcome page template
│   │   ├── summary-page.blp        # Summary page template
│   │   └── wizard-page.blp         # Generic page template
│   ├── ui/                         # Compiled UI files (generated)
│   └── wizard.gresource.xml        # GResource definition
└── meson.build                     # Build configuration
```

## Blueprint Files

### wizard-window.blp
Main application window with:
- Adwaita ApplicationWindow as root
- HeaderBar with window title
- Carousel for page navigation
- CarouselIndicatorDots for page indication

### wizard-page.blp
Generic wizard page template with:
- Adw.Clamp for responsive layout
- Title and subtitle labels
- Action button
- Consistent Adwaita styling

### welcome-page.blp & summary-page.blp
Specific page implementations using Adw.StatusPage for visual appeal.

## Build Process

The Meson build system automatically:

1. **Detects blueprint-compiler**: Checks if the tool is available
2. **Compiles .blp → .ui**: Batch compiles all Blueprint files
3. **Creates GResource bundle**: Packages compiled UI files into a single resource file
4. **Installs resources**: Installs the bundle to the appropriate location

### Build Configuration

In `meson.build`:

```meson
blueprint_compiler = find_program('blueprint-compiler', required: false)

if blueprint_compiler.found()
  blp_files = files(
    'resources/blueprints/wizard-window.blp',
    'resources/blueprints/welcome-page.blp',
    'resources/blueprints/summary-page.blp',
    'resources/blueprints/wizard-page.blp',
  )

  compiled_ui = custom_target(
    'compile-blueprints',
    input: blp_files,
    output: ['wizard-window.ui', 'welcome-page.ui', ...],
    command: [blueprint_compiler, 'batch-compile', '@OUTDIR@', ...],
    build_by_default: true,
  )

  wizard_resources = gnome.compile_resources(
    'wizard-resources',
    'resources/wizard.gresource.xml',
    dependencies: compiled_ui,
    install: true,
    install_dir: pkgdatadir / 'Wizard',
  )
endif
```

## Python Integration

### Loading Resources

```python
from cloud.ivanbotty.Wizard.blueprint_ui import load_wizard_resources

# Load the Wizard GResource bundle
load_wizard_resources()
```

### Using Blueprint UI Components

```python
from cloud.ivanbotty.Wizard.blueprint_ui import WizardWindowBlueprint, WizardPageBlueprint

# Create main window
window = WizardWindowBlueprint(application=app)

# Create a wizard page
page = WizardPageBlueprint(
    title="Welcome",
    subtitle="Let's get started!",
    button_text="Next",
    callback=on_next_clicked
)

# Add page to carousel
window.carousel.append(page)
```

### Fallback Support

The implementation includes automatic fallback to programmatic UI creation if:
- Blueprint compiler is not available during build
- Resource files cannot be loaded at runtime
- GResource loading fails

This ensures the application remains functional even without Blueprint support.

## Design Guidelines

The Blueprint files follow GNOME Adwaita design principles:

### Layout
- Use `Adw.Clamp` for responsive, centered content (max-width: 640px)
- Apply consistent margins: 48px vertical, 32px horizontal
- Use 24px spacing between major elements

### Typography
- Title: `title-1` CSS class or `size='xx-large' weight='bold'`
- Subtitle: Regular text with `dim-label` CSS class
- Center-aligned text with word wrapping

### Buttons
- Primary action: `suggested-action` CSS class
- Pill shape: `pill` CSS class
- Center-aligned with 12px top margin

### Theming
- All UI components automatically support light/dark themes
- Symbolic icons (e.g., `system-software-install-symbolic`)
- Consistent with GNOME HIG (Human Interface Guidelines)

### Internationalization
- All user-visible strings marked as translatable with `_("text")`
- Supports dynamic language switching

## Example Usage

See `app_blueprint_example.py` for a complete example of integrating Blueprint UI with the existing Wizard application.

### Running the Example

```bash
# Build the project
meson setup builddir
meson compile -C builddir

# Install (may require sudo)
meson install -C builddir

# Run the Blueprint-based wizard
python3 -m cloud.ivanbotty.Wizard.app_blueprint_example
```

## Migration Path

To migrate the existing `app.py` to use Blueprint UI:

1. Replace `Window` import with `WizardWindowBlueprint`
2. Replace `Page.make_page()` calls with `WizardPageBlueprint` instances
3. Load resources at application startup with `load_wizard_resources()`
4. Test with and without Blueprint compiler to ensure fallback works

## Requirements

### Build-time
- `blueprint-compiler` >= 0.4.0 (optional, graceful fallback)
- `meson` >= 0.59.0
- `gtk4` >= 4.0

### Runtime
- `python3` >= 3.8
- `python3-gi` with GTK 4.0 and Adwaita 1 bindings
- GResource support in GLib

## Benefits

1. **Separation of Concerns**: UI layout separate from business logic
2. **Maintainability**: Declarative UI is easier to understand and modify
3. **Adwaita Compliance**: Automatic adherence to GNOME design patterns
4. **Tooling**: Better IDE support for UI editing (GNOME Builder)
5. **Performance**: Compiled UI loads faster than programmatic construction
6. **Consistency**: Enforced design patterns across all pages

## Troubleshooting

### Blueprint compiler not found
The build will issue a warning but continue. The application will use fallback UI.

### GResource not loading
Check that:
- The build installed resources to the correct location
- `pkgdatadir` is accessible
- The application has read permissions

Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

### UI looks different
If Blueprint UI and fallback UI look different:
- Verify Blueprint compiler version
- Check for CSS class support in your GTK version
- Ensure Adwaita stylesheet is loaded

## Future Enhancements

- [ ] Add more specialized page templates
- [ ] Create custom widgets in Blueprint
- [ ] Add animations and transitions
- [ ] Implement keyboard navigation
- [ ] Add accessibility labels
- [ ] Create Blueprint-based preferences dialog
