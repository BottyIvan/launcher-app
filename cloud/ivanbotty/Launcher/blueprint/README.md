# Blueprint Design Pattern

This document explains the blueprint design pattern implementation in the Launcher application, which simplifies UI creation and improves maintainability.

## Overview

The blueprint design pattern provides a centralized, consistent approach to creating UI components. It addresses several key challenges:

1. **Consistency**: Ensures all UI components follow the same styling and spacing rules
2. **Maintainability**: Changes to styling can be made in one place
3. **Scalability**: New components can be easily added following established patterns
4. **Usability**: Reduces code duplication and makes UI code more readable

## Architecture

The blueprint system consists of three main components:

### 1. StyleBlueprint (`blueprint/style_blueprint.py`)

Centralized style management that provides:
- **Layout configurations**: Compact and default layout presets
- **Spacing values**: Standardized spacing (xs, sm, md, lg, xl, xxl)
- **Size presets**: Icon sizes and component dimensions
- **Theme management**: Adwaita theme initialization and configuration

**Key features:**
```python
# Get current layout configuration
layout = style_blueprint.get_layout()

# Apply standard margins to any widget
style_blueprint.apply_margins(widget)

# Apply consistent spacing to box containers
style_blueprint.apply_spacing(box, "md")

# Get standardized icon sizes
icon_size = style_blueprint.get_icon_size("md")
```

### 2. ComponentRegistry (`blueprint/component_registry.py`)

Factory for creating standardized UI components with consistent styling:

- **Buttons**: Icon buttons, text buttons, tag buttons
- **Labels**: With bold, dim, alignment options
- **Boxes**: Vertical/horizontal containers with spacing
- **Icons**: Themed icons with size presets
- **Entries**: Search/input fields with icons
- **List boxes**: For displaying results
- **Scrolled windows**: For scrollable content

**Example usage:**
```python
# Create a button with icon and tooltip
button = components.create_icon_button(
    icon_name="applications-system-symbolic",
    tooltip="Open Preferences",
    css_classes=["flat"]
)

# Create a label with specific styling
label = components.create_label(
    text="Hello World",
    bold=True,
    align_start=True
)

# Create a box container with spacing
box = components.create_box(
    orientation=Gtk.Orientation.VERTICAL,
    spacing="md"
)
```

### 3. UIBlueprint (`blueprint/ui_blueprint.py`)

High-level interface for creating complete UI layouts:

- **Window creation**: Consistent window sizing and configuration
- **Search bar**: Standardized search entry with icons
- **Main list view**: Result display area
- **Footer layout**: Bottom toolbar with shortcuts
- **Progress bar**: Loading indicators
- **Main layout**: Complete application layout assembly

**Example usage:**
```python
# Initialize blueprint
ui_blueprint = UIBlueprint()

# Create main window
window = ui_blueprint.create_window(app)

# Create search bar
search_entry = ui_blueprint.create_search_bar()

# Create main list view
list_view = ui_blueprint.create_main_list_view()

# Create footer
footer = ui_blueprint.create_footer_layout(app)

# Assemble main layout
main_layout = ui_blueprint.create_main_layout(
    search_entry, progress_bar, list_view, footer
)
```

## Benefits

### Before Blueprint Pattern
```python
# Scattered styling logic
entry = Gtk.Entry()
entry.set_size_request(UI_CONFS[PREFERENCES]["entry_width"], 
                       UI_CONFS[PREFERENCES]["entry_height"])
entry.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
entry.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
entry.add_css_class("flat")
entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, 
                              "system-search-symbolic")
# ... more configuration
```

### After Blueprint Pattern
```python
# Clean, consistent API
entry = ui_blueprint.create_search_bar()
```

### Key Improvements

1. **Reduced Code Duplication**: Common UI patterns are defined once
2. **Easier Maintenance**: Styling changes require updates in one place
3. **Better Consistency**: All components follow the same design rules
4. **Improved Readability**: Intent is clearer with descriptive method names
5. **Faster Development**: New features can reuse existing components

## Integration with Existing Code

The blueprint pattern is designed to work alongside existing code:

1. **Backward Compatibility**: Existing widgets still work without blueprint
2. **Gradual Adoption**: Components can be migrated incrementally
3. **Optional Usage**: Blueprint is available but not mandatory

## Usage in Application

### Main Application (app.py)

```python
# Initialize blueprint
self.ui_blueprint = UIBlueprint()

# Create widgets using blueprint
self.progress_bar = self.ui_blueprint.create_progress_bar("Loading...")
self.view = self.ui_blueprint.create_main_list_view()
self.entry = SearchEntry(ui_blueprint=self.ui_blueprint)

# Create window and layout
self.win = self.ui_blueprint.create_window(self)
footer = self.ui_blueprint.create_footer_layout(self)
main_layout = self.ui_blueprint.create_main_layout(
    self.entry, self.progress_bar, self.view, footer
)
```

### Row Widget (widget/row.py)

```python
# Use blueprint for consistent styling
self.ui_blueprint = UIBlueprint()

# Create components using blueprint
row_box = self.ui_blueprint.components.create_box(
    orientation=Gtk.Orientation.HORIZONTAL,
    spacing="lg"
)

# Apply margins using blueprint
self.ui_blueprint.style.apply_margins(row_box, layout_margins)

# Create tag button
tag_button = self.ui_blueprint.components.create_tag_button(tag)
```

## Extending the Blueprint

To add new component types:

1. Add factory method to `ComponentRegistry`
2. Use `StyleBlueprint` for consistent styling
3. Document the new component type

Example:
```python
def create_my_component(self, param1, param2):
    """Create a new component type."""
    widget = Gtk.MyWidget()
    self.style.apply_margins(widget)
    self.style.apply_css_classes(widget, ["my-class"])
    return widget
```

## Testing

The blueprint pattern simplifies testing:
- Mock `StyleBlueprint` for different layouts
- Test component creation independently
- Verify consistent styling across components

## Future Enhancements

Potential improvements:
1. Support for custom themes beyond compact/default
2. Animation blueprints for transitions
3. Responsive layout adaptations
4. Component state management
5. Accessibility enhancements

## Migration Guide

To migrate existing widgets to use blueprint:

1. Import `UIBlueprint` at the top of your file
2. Create blueprint instance: `self.ui_blueprint = UIBlueprint()`
3. Replace manual widget creation with blueprint methods
4. Remove direct config imports where possible
5. Test the widget to ensure behavior is unchanged

## Conclusion

The blueprint design pattern provides a solid foundation for building consistent, maintainable UIs in the Launcher application. By centralizing styling and component creation, it makes the codebase easier to understand and extend while improving the user experience through consistent design.
