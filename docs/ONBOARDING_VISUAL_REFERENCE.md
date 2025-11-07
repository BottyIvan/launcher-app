# Onboarding Visual Reference

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      First Launch                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │  Check Preferences DB  │
          └────────┬───────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
   show_welcome_wizard   show_welcome_wizard
       = True                = False
          │                 │
          ▼                 ▼
  ┌──────────────┐   ┌──────────────┐
  │    Wizard    │   │     Main     │
  │  Application │   │ Application  │
  └──────┬───────┘   └──────────────┘
         │
         ▼
    Page 1: Welcome
         │
         ▼
    Page 2: Search
         │
         ▼
    Page 3: Keyboard
         │
         ▼
    Page 4: Personalize
         │
         ▼
    Page 5: Privacy
         │
         ▼
    Mark Complete
         │
         ▼
   Launch Main App
```

## Page Structure

Each onboarding page follows this visual hierarchy:

```
┌─────────────────────────────────────┐
│                                     │
│           ┌─────────┐               │
│           │  ICON   │  64px         │
│           └─────────┘               │
│                                     │
│         Page Title                  │
│         (x-large, bold)             │
│                                     │
│    ┌─────────────────────────┐     │
│    │                         │     │
│    │   Description Text      │     │
│    │   (regular, dim-label)  │     │
│    │                         │     │
│    │   • Bullet points       │     │
│    │   • Feature highlights  │     │
│    │                         │     │
│    └─────────────────────────┘     │
│                                     │
│       ┌─────────────┐               │
│       │   BUTTON    │ (pill)        │
│       └─────────────┘               │
│                                     │
│   ○ ○ ● ○ ○  (page indicators)     │
│                                     │
└─────────────────────────────────────┘
```

## Spacing and Margins

```
Top Margin:     48px
Bottom Margin:  48px
Side Margins:   32px
Element Gap:    20px
Icon to Title:  12px
Title to Desc:  12px
Desc to Button: 24px
Button to Dots: 16px
```

## Typography Scale

| Element     | Size     | Weight | Color      |
|-------------|----------|--------|------------|
| Icon        | 64px     | N/A    | Accent     |
| Title       | x-large  | Bold   | Default    |
| Description | Medium   | Normal | Dim-label  |
| Button      | Medium   | Normal | White      |

## Button States

```
┌─────────────────────┐
│  Get Started        │  Default (suggested-action)
└─────────────────────┘

┌─────────────────────┐
│  Get Started        │  Hover (lighter blue)
└─────────────────────┘

┌─────────────────────┐
│  Get Started        │  Active (darker blue)
└─────────────────────┘

┌─────────────────────┐
│  Get Started        │  Focus (outline ring)
└─────────────────────┘
```

## Page Transitions

```
Current Page          Next Page
┌─────────┐          ┌─────────┐
│ ████████│          │         │
│ ████████│  ───→    │         │
│ ████████│          │         │
└─────────┘          └─────────┘
     ↓                    ↓
Fade out 200ms      Fade in 200ms
  + Slide left        + Slide right
```

Animation properties:
- Duration: 200-300ms (native Adwaita timing)
- Easing: Spring physics (Adw.Carousel default)
- Direction: Horizontal slide with spring bounce

## Color Tokens

### Light Mode
- Background: `@window_bg_color`
- Text: `@window_fg_color`
- Dim Text: `@dim_label`
- Accent: `@accent_bg_color`
- Button: `@accent_bg_color`

### Dark Mode
- Background: `@window_bg_color`
- Text: `@window_fg_color`
- Dim Text: `@dim_label`
- Accent: `@accent_bg_color`
- Button: `@accent_bg_color`

All colors automatically adapt to system theme.

## Responsive Behavior

### Default Window Size
- Width: 850px
- Height: 580px
- Min Width: 600px
- Min Height: 400px

### Content Constraints
- Max Content Width: 640px (via Adw.Clamp)
- Centered horizontally
- Centered vertically

## Accessibility Features

### Keyboard Navigation
```
Tab         → Move to next focusable element
Shift+Tab   → Move to previous focusable element
Enter       → Activate focused button
Space       → Activate focused button
Arrow Left  → Previous page (on carousel)
Arrow Right → Next page (on carousel)
Escape      → Close window
```

### Screen Reader Announcements
- Page title announced on page change
- Button labels announced on focus
- Page indicators announce "Page X of 5"

### High Contrast Support
- Icon sizes maintained
- Button contrast meets WCAG AAA
- Text contrast meets WCAG AAA
- Focus indicators clearly visible

### Reduced Motion
- Respects `prefers-reduced-motion`
- Instant page changes (no animation)
- Static transitions only

## Icon Mapping

| Page | Icon Name                    | Symbolic | Size |
|------|------------------------------|----------|------|
| 1    | applications-system-symbolic | Yes      | 64px |
| 2    | system-search-symbolic       | Yes      | 64px |
| 3    | input-keyboard-symbolic      | Yes      | 64px |
| 4    | emblem-system-symbolic       | Yes      | 64px |
| 5    | security-high-symbolic       | Yes      | 64px |

All icons are from the standard icon theme and fallback gracefully.

## Integration Points

### Database Preferences

```
┌──────────────────────────────────────┐
│  Preference Key          Value Type  │
├──────────────────────────────────────┤
│  show_welcome_wizard     Boolean     │
│  onboarding_completed_at String      │
└──────────────────────────────────────┘
```

### Config Functions

```python
# Check if wizard should run
should_show_onboarding() -> bool

# Mark wizard as complete
mark_onboarding_complete() -> None

# Allow wizard to run again
reset_onboarding() -> None
```

### Preferences Dialog

```
┌─────────────────────────────────────┐
│  Preferences                        │
├─────────────────────────────────────┤
│                                     │
│  Welcome Wizard                     │
│  ┌───────────────────────────────┐ │
│  │ Run Setup Again         ▶     │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Implementation Checklist

Layout & Structure:
- [x] Use Adw.Carousel for page transitions
- [x] Add Adw.CarouselIndicatorDots for progress
- [x] Use Adw.Clamp to constrain content width
- [x] Implement responsive margins and spacing

Content:
- [x] 5 pages covering key features
- [x] Clear, concise descriptions
- [x] Friendly, welcoming tone
- [x] Proper visual hierarchy

Visual Design:
- [x] 64px symbolic icons
- [x] x-large bold titles
- [x] dim-label for descriptions
- [x] pill-style action buttons
- [x] Proper spacing (48/32/20/12px)

Integration:
- [x] Database tracking (show_welcome_wizard)
- [x] Completion timestamp
- [x] Reset functionality in Preferences
- [x] Launch main app after completion

Accessibility:
- [x] Keyboard navigation
- [x] Native GTK accessibility
- [x] Semantic HTML structure
- [x] High contrast compatible
- [x] Reduced motion support

## Testing Scenarios

1. **First Launch**
   - Launch app for first time
   - Wizard should appear automatically
   - All 5 pages should be navigable
   - Final button should launch main app

2. **Subsequent Launches**
   - Launch app after completing wizard
   - Main app should appear directly
   - No wizard shown

3. **Reset and Re-run**
   - Open Preferences (Ctrl+,)
   - Click "Run Setup Again"
   - Close and relaunch app
   - Wizard should appear again

4. **Theme Compatibility**
   - Test in light mode
   - Test in dark mode
   - Test with high contrast
   - Icons and colors should adapt

5. **Keyboard Navigation**
   - Tab through all elements
   - Activate buttons with Enter/Space
   - Navigate carousel with arrows
   - Close with Escape

6. **Responsive Layout**
   - Resize window to minimum
   - Content should remain readable
   - No horizontal scrolling
   - Clamp maintains max width

---

For implementation details, see [ONBOARDING_FLOW.md](./ONBOARDING_FLOW.md)
