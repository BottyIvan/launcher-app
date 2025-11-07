# UI Enhancement Visual Reference

This document provides a visual description of the UI enhancements made to the Launcher application.

## Before and After Comparison

### Main Window

**Before:**
- Basic window with simple search bar
- Plain list of results
- No visual hierarchy
- Basic spacing and margins

**After:**
- Modern window with enhanced search bar featuring:
  - Rounded corners (12px border-radius)
  - Subtle box shadow for depth
  - Dynamic clear button
  - Larger size (52px height in default mode)
- Results list with:
  - Smooth slide-in animations
  - Hover effects with background color changes
  - Color-coded category tags
  - Better icon presentation (32px with shadows)
- Improved spacing following 12px grid system

### Search Entry

```
┌─────────────────────────────────────────────────────────────┐
│  🔍  Type to search...                                   ✕  │  ← Rounded, shadowed
└─────────────────────────────────────────────────────────────┘
    ↑                                                        ↑
  Search icon                                       Clear button (appears on input)
```

Visual characteristics:
- Background: @headerbar_bg_color (light gray in light theme)
- Border radius: 12px
- Box shadow: 0 2px 8px rgba(0,0,0,0.12)
- On focus: Enhanced shadow with accent color hint
- Height: 52px (default), 40px (compact)

### Results List

```
┌─────────────────────────────────────────────────────────────┐
│  [Icon]  Application Name                        [APP]      │  ← Row with hover effect
│          Brief description of the application                │
├─────────────────────────────────────────────────────────────┤
│  [Icon]  Calculator                              [MATH]     │
│          Quick math calculations                             │
├─────────────────────────────────────────────────────────────┤
│  [Icon]  AI Assistant                             [AI]      │
│          Ask questions and get answers                       │
└─────────────────────────────────────────────────────────────┘
```

Visual characteristics:
- Icon size: 32px with 8px border-radius and shadow
- Icon container: 40x40px for consistent spacing
- App name: 15px, font-weight 600, @window_fg_color
- Description: 13px, @window_fg_color with 0.65 opacity
- Category tags: Pill-shaped with type-specific colors
  - APP: Blue (@blue_3 with 15% opacity)
  - MATH: Green (@green_3 with 15% opacity)
  - AI: Purple (@purple_3 with 15% opacity)
  - CMD: Orange (@orange_3 with 15% opacity)
  - FILE: Yellow (@yellow_3 with 15% opacity)

Row interactions:
- Hover: Background alpha(@accent_bg_color, 0.08)
- Selected: Background alpha(@accent_bg_color, 0.15)
- Icon scale on hover: 1.05x

### Footer

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙                          ↑↓ Navigate  ↵ Select  Esc Close│
└─────────────────────────────────────────────────────────────┘
    ↑                          ↑────────────────────────────────
  Preferences                     Keyboard shortcuts (right-aligned)
```

Visual characteristics:
- Background: @headerbar_bg_color
- Border-top: 1px solid alpha(@shade_color, 0.08)
- Shortcut hints: Rounded boxes (6px) with monospace font
- Preferences button: Circular with preferences icon
- Height: Compact, non-intrusive

### Preferences Dialog

```
┌─────────────────────────────────────────────────────────────┐
│  Preferences                                            ✕   │
├─────────────────────────────────────────────────────────────┤
│  General | Appearance | Extensions | API Keys               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─ Appearance ────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  Layout                                              │   │
│  │  Customize the application window appearance         │   │
│  │                                                       │   │
│  │  Compact Layout                              [●] On  │   │
│  │  Use a smaller, more condensed interface             │   │
│  │                                                       │   │
│  │  Note: Some changes may require restart              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

Pages:
1. **General** - About and app info
2. **Appearance** - Layout settings (compact/default)
3. **Extensions** - Enable/disable features
4. **API Keys** - Configure external services

### Keyboard Shortcuts Overlay

```
┌─────────────────────────────────────────────────────────────┐
│  Keyboard Shortcuts                                     ✕   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Navigation                                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Type              Search applications and commands │     │
│  │  ↑ / ↓             Navigate results                │     │
│  │  Enter             Launch selected item            │     │
│  │  Escape            Close window                     │     │
│  │  Backspace         Clear search                     │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Application                                                 │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Ctrl+,            Open preferences                 │     │
│  │  Ctrl+Q            Quit application                 │     │
│  │  Ctrl+? / F1       Show this help                   │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

Access via: Ctrl+? or F1

## Color Palette

The UI uses Adwaita color tokens for automatic dark/light theme compatibility:

### Light Theme Colors
- Window background: @window_bg_color (#fafafa)
- Text: @window_fg_color (#2e3436)
- Accent: @accent_bg_color (System accent, typically #3584e4 blue)
- Header: @headerbar_bg_color (#ebebeb)
- Shadows: @shade_color with varying opacity

### Dark Theme Colors
- Window background: @window_bg_color (#242424)
- Text: @window_fg_color (#ffffff)
- Accent: @accent_bg_color (Lighter variant for dark theme)
- Header: @headerbar_bg_color (#303030)
- Shadows: @shade_color with varying opacity

## Animations

All animations use smooth easing: `cubic-bezier(0.25, 0.46, 0.45, 0.94)`

### Transition Timings
- UI interactions: 150ms (hover, focus)
- Search entry: 200ms (shadow, background)
- Row animations: 200ms (slide-in-up)
- Window: 150ms (fade-in)

### Animation Effects
1. **Slide-in-up**: Results appear from 10px below with fade
2. **Fade-in**: Window appears smoothly
3. **Scale**: Icons scale to 1.05x on hover
4. **Background**: Smooth color transitions on hover/select

## Responsive Behavior

### Default Mode (850x580)
- Full spacing (20px horizontal, 16px vertical)
- Larger entry (810x52)
- Comfortable icon sizes (32px)
- Maximum readability

### Compact Mode (700x400)
- Reduced spacing (10px all around)
- Smaller entry (660x40)
- Same icon sizes maintained
- Optimized for smaller screens

### Minimum Size (600x400)
- Enforced via window constraints
- Ensures usability on all screen sizes
- Scrollable results area

## Accessibility Features

### Visual
- High contrast text (follows system theme)
- Clear focus indicators
- Minimum 40px touch targets
- Proper text sizing (13-15px for content)

### Keyboard
- All features keyboard accessible
- Clear shortcut indicators
- Logical tab order
- Focus visible on all interactive elements

### Responsive
- Flexible layouts
- Minimum size constraints
- Compact mode for smaller displays
- Works on HiDPI displays

## Design References

The UI draws inspiration from:

1. **KDE Krunner** - Clean search-focused interface
2. **PowerToys Run** - Category tags and result organization
3. **Raycast** - Modern aesthetics and smooth animations
4. **macOS Spotlight** - Minimalist design and keyboard-first approach
5. **GNOME HIG** - Color tokens, spacing, and widget usage

## CSS Architecture

The stylesheet (`style.css`) is organized into sections:

1. **Window and General Layout** - Base styling
2. **Search Entry Enhancements** - Input field styling
3. **Results List Styling** - Row and list presentation
4. **Row Content** - Icons and text
5. **Category Tags** - Color-coded tags
6. **Progress Bar** - Loading indicator
7. **Footer** - Keyboard hints
8. **Preferences Dialog** - Settings UI
9. **Scrollbar** - Custom scrollbar styling
10. **Animations** - Keyframes and transitions
11. **Utility Classes** - Reusable styles

All styles use Adwaita color tokens for automatic theming.

## Implementation Notes

- CSS loaded from GResource for efficiency
- Animations use GPU-accelerated properties
- No inline styles - all via CSS classes
- Follows GTK4 best practices
- Compatible with Wayland and X11
