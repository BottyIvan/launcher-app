# Onboarding Flow Documentation

## Overview

The Launcher application features a modern, user-friendly onboarding experience designed to welcome first-time users and introduce them to the application's key features. The onboarding flow is built using GTK4/Adwaita components and follows the GNOME Human Interface Guidelines (HIG).

## Design Philosophy

The onboarding experience is designed with these principles:

- **Clear and Guided**: Each step introduces one concept at a time
- **Minimal and Concise**: Short, scannable content that respects user time
- **Native and Accessible**: Uses Adwaita components for consistency and accessibility
- **Privacy-Focused**: Emphasizes local storage and no data collection
- **Skippable**: Users can complete the wizard at their own pace

## Architecture

### Components

#### 1. WelcomeWizard (`cloud/ivanbotty/Wizard/app.py`)

The main application class that manages the onboarding flow:

- Extends `Adw.Application`
- Loads wizard configuration from `wizard.yaml`
- Manages page transitions using `Adw.Carousel`
- Handles wizard completion and launches main application

**Key Methods:**
- `on_next()`: Navigate to next page
- `on_prev()`: Navigate to previous page
- `on_finish()`: Complete wizard and mark onboarding as done

#### 2. Page Component (`cloud/ivanbotty/Wizard/components/page.py`)

Factory class for creating individual onboarding pages:

- Creates `Adw.Clamp` containers for consistent maximum width
- Supports optional icons for visual appeal
- Uses native Adwaita typography and spacing
- Provides suggested-action buttons with pill styling

**Features:**
- Icon support (64px, themed)
- Title with x-large bold text
- Description with dim styling for hierarchy
- Centered action button with pill style
- Responsive layout with proper margins

#### 3. Configuration (`cloud/ivanbotty/Launcher/config/config.py`)

Helper functions for tracking onboarding state:

- `should_show_onboarding()`: Check if wizard should be shown
- `mark_onboarding_complete()`: Mark wizard as completed with timestamp
- `reset_onboarding()`: Allow users to re-run the wizard

### Content Configuration

Onboarding content is defined in `cloud/ivanbotty/Launcher/resources/wizard.yaml`:

```yaml
pages:
  - title: "Page Title"
    icon: "icon-name-symbolic"  # Optional
    description: |
      Multi-line description with markdown support.
      • Bullet points for features
      • Clear, concise language
    button_label: "Next"  # Or "Get Started", "Launch Launcher"
```

## Onboarding Flow

### Page 1: Welcome

**Purpose**: Welcome users and introduce the application

**Content:**
- Application name and tagline
- Brief value proposition
- Inviting call-to-action

**Icon**: `applications-system-symbolic`

### Page 2: Lightning-Fast Search

**Purpose**: Introduce core search functionality

**Content:**
- Instant search capability
- Fuzzy matching
- Application coverage (native and Flatpak)
- Built-in calculator feature

**Icon**: `system-search-symbolic`

### Page 3: Keyboard-First Design

**Purpose**: Teach basic keyboard shortcuts

**Content:**
- Type to search
- Arrow keys for navigation
- Enter to launch
- Escape to close
- Ctrl+? for help

**Icon**: `input-keyboard-symbolic`

### Page 4: Personalize Your Experience

**Purpose**: Introduce customization options

**Content:**
- Layout options (compact/spacious)
- Extension modules
- Local preference storage
- Settings shortcut (Ctrl+,)

**Icon**: `emblem-system-symbolic`

### Page 5: Privacy First

**Purpose**: Emphasize privacy and complete onboarding

**Content:**
- No telemetry or tracking
- Local data storage
- Privacy-respecting design
- Final call-to-action

**Icon**: `security-high-symbolic`

## User Experience Features

### Visual Elements

1. **Page Indicators**
   - `Adw.CarouselIndicatorDots` shows progress
   - Centered below carousel
   - Automatically updates on page change

2. **Smooth Transitions**
   - Native carousel animations
   - Mouse drag support enabled
   - Scroll wheel navigation enabled
   - Smooth spring physics

3. **Typography Hierarchy**
   - Icons: 64px, themed with accent color
   - Titles: x-large, bold
   - Descriptions: Regular, dim-label class
   - Consistent 20px spacing between elements

4. **Button Styling**
   - `suggested-action` class (blue)
   - `pill` class for rounded ends
   - 200px minimum width
   - Centered alignment

### Accessibility

- Native GTK accessibility support
- Proper ARIA labels via Adwaita widgets
- Keyboard navigation (Tab, Shift+Tab)
- Screen reader compatible
- High contrast theme support
- Respects reduced motion preferences

### Theme Compatibility

- Automatic light/dark mode switching
- Uses semantic color tokens
- `accent` class for icons
- `dim-label` class for secondary text
- Follows system theme preferences

## Integration with Main Application

### First Launch Detection

The launcher checks for first launch in `__main__.py`:

```python
if db.get_pref("show_welcome_wizard", True) is True:
    db.set_pref("show_welcome_wizard", False)
    app = WelcomeWizard(app="cloud.ivanbotty.Wizard")
else:
    app = App(app="cloud.ivanbotty.Launcher")
```

### Completion Tracking

When the wizard is completed:

1. `mark_onboarding_complete()` is called
2. Preference `show_welcome_wizard` set to `False`
3. Timestamp stored in `onboarding_completed_at`
4. Main application launches automatically

### Re-running Onboarding

Users can re-run the onboarding from Preferences:

1. Navigate to Preferences (Ctrl+,)
2. Go to "General" page
3. Click "Run Setup Again" in "Welcome Wizard" group
4. Wizard will show on next application launch

## Development Guidelines

### Adding New Pages

1. Edit `wizard.yaml`:
   ```yaml
   - title: "Your Title"
     icon: "icon-name-symbolic"  # Optional
     description: |
       Your description
     button_label: "Next"
   ```

2. No code changes needed - pages are generated dynamically

### Customizing Page Appearance

Edit `Page.make_page()` in `page.py`:
- Adjust spacing values
- Modify icon size
- Change text styling
- Update button appearance

### Modifying Carousel Behavior

Edit `WelcomeWizard.do_activate()`:
- Enable/disable mouse drag: `set_allow_mouse_drag()`
- Enable/disable scroll wheel: `set_allow_scroll_wheel()`
- Change indicator style (dots vs. lines)

## Best Practices

### Content Writing

- **Be Concise**: Each page should be scannable in 5-10 seconds
- **Use Bullet Points**: Break up text for readability
- **Active Voice**: "Search for apps" not "Apps can be searched"
- **Friendly Tone**: Welcoming but professional
- **Feature Benefits**: Focus on what users can do, not technical details

### Visual Design

- **One Concept Per Page**: Don't overload with information
- **Consistent Icons**: Use symbolic icons from standard icon theme
- **Proper Spacing**: Follow Adwaita spacing guidelines (12px, 20px, 24px)
- **Hierarchy**: Clear visual distinction between title and description

### Technical Considerations

- **No External Dependencies**: Use only GTK4/Adwaita APIs
- **Resource Efficient**: Lazy load pages, minimal memory footprint
- **Fast Loading**: YAML parsing is quick, pages render instantly
- **Error Handling**: Graceful degradation if YAML is malformed

## Testing

### Manual Testing Checklist

- [ ] First launch shows wizard automatically
- [ ] All pages display correctly
- [ ] Icons render properly in light/dark themes
- [ ] Page indicators update on navigation
- [ ] Carousel navigation works (mouse, keyboard, scroll)
- [ ] "Next" buttons advance to next page
- [ ] Final button launches main application
- [ ] Onboarding completion is tracked
- [ ] "Run Setup Again" in Preferences works
- [ ] Wizard shows again after reset

### Accessibility Testing

- [ ] Navigate with Tab/Shift+Tab
- [ ] Buttons activate with Enter/Space
- [ ] Screen reader announces content
- [ ] High contrast mode displays correctly
- [ ] Reduced motion respected (if configured)

## Future Enhancements

Potential improvements for future versions:

1. **Contextual Steps**: Detect environment (Flatpak, system install) and adjust content
2. **AI Detection**: Show/hide AI-related content based on API key availability
3. **Skip Button**: Allow users to skip wizard entirely
4. **Mini Tours**: Contextual tooltips after first launch
5. **Interactive Elements**: Let users try features during onboarding
6. **Progress Persistence**: Resume from last page if wizard is interrupted
7. **Localization**: Multi-language support for international users
8. **Onboarding Analytics**: Track completion rates (privacy-preserving)

## References

- [GNOME Human Interface Guidelines](https://developer.gnome.org/hig/)
- [Adwaita Carousel Documentation](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/class.Carousel.html)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [GNOME Application Examples](https://gitlab.gnome.org/GNOME):
  - GNOME Boxes: Comprehensive onboarding flow
  - Fragments: Simple, focused wizard
  - Podcasts: Multi-step setup process

## Changelog

### Version 0.0.1 (Initial Implementation)

- Implemented `Adw.Carousel`-based onboarding flow
- Created 5-page introduction sequence
- Added page indicators with dots
- Integrated with configuration system
- Added "Run Setup Again" in Preferences
- Created comprehensive documentation
- Designed with accessibility in mind
- Followed Adwaita design patterns

---

For questions or contributions related to the onboarding flow, please refer to the [Contributing Guide](../CONTRIBUTING) or open an issue on GitHub.
