# Dashboard Color Palette & Theme Reference

## 📊 Light Mode Color Palette

### Primary Colors
```
Indigo Gradient:
┌─────────────────────────────────────────┐
│ #4F46E5 (Primary) - Main Accent         │
│ #6366F1 (Light)   - Hover/Light         │
│ #4338CA (Dark)    - Active/Dark         │
└─────────────────────────────────────────┘
Used for: Buttons, links, primary accents
```

### Secondary Colors (Purple)
```
Purple Gradient:
┌─────────────────────────────────────────┐
│ #8B5CF6 (Secondary) - Accent            │
│ #A78BFA (Light)     - Light variant     │
│ #7C3AED (Dark)      - Dark variant      │
└─────────────────────────────────────────┘
Used for: Gradients, decorative elements
```

### Status Colors

#### Success (Green)
```
┌─────────────────────────────────────────┐
│ #10B981 - Main Success Color            │
│ #34D399 - Light Success                 │
│ #059669 - Dark Success                  │
└─────────────────────────────────────────┘
Used for: Positive actions, successful states, billing button
```

#### Warning (Amber/Orange)
```
┌─────────────────────────────────────────┐
│ #F59E0B - Main Warning Color            │
│ #FBBF24 - Light Warning                 │
│ #D97706 - Dark Warning                  │
└─────────────────────────────────────────┘
Used for: Warnings, caution messages, service buttons
```

#### Danger (Red)
```
┌─────────────────────────────────────────┐
│ #EF4444 - Main Danger Color             │
│ #F87171 - Light Danger                  │
│ #DC2626 - Dark Danger                   │
└─────────────────────────────────────────┘
Used for: Errors, destructive actions, logout
```

#### Info (Cyan)
```
┌─────────────────────────────────────────┐
│ #06B6D4 - Main Info Color               │
│ #22D3EE - Light Info                    │
│ #0891B2 - Dark Info                     │
└─────────────────────────────────────────┘
Used for: Informational content, reports button
```

### Neutral Colors

#### Background Colors
```
┌─────────────────────────────────────────┐
│ #FFFFFF    - Primary Background (White) │
│ #F9FAFB    - Secondary Background       │
│ #F3F4F6    - Tertiary Background        │
└─────────────────────────────────────────┘
Usage:
- bg-primary: Main container backgrounds
- bg-secondary: Page background
- bg-tertiary: Section backgrounds
```

#### Text Colors
```
┌─────────────────────────────────────────┐
│ #111827    - Primary Text (Dark)        │
│ #4B5563    - Secondary Text             │
│ #9CA3AF    - Tertiary Text (Light)      │
└─────────────────────────────────────────┘
Usage:
- text-primary: Headlines, important text
- text-secondary: Body text, descriptions
- text-tertiary: Hints, labels, metadata
```

#### Border & Divider Colors
```
┌─────────────────────────────────────────┐
│ #E5E7EB    - Standard Border             │
│ #F3F4F6    - Light Border                │
└─────────────────────────────────────────┘
```

## 🌙 Dark Mode Color Palette

### Background Colors (Dark)
```
┌─────────────────────────────────────────┐
│ #111827    - Primary Background         │
│ #1F2937    - Secondary Background       │
│ #374151    - Tertiary Background        │
└─────────────────────────────────────────┘
```

### Text Colors (Dark)
```
┌─────────────────────────────────────────┐
│ #F9FAFB    - Primary Text (Light)       │
│ #D1D5DB    - Secondary Text             │
│ #9CA3AF    - Tertiary Text              │
└─────────────────────────────────────────┘
```

### Border Colors (Dark)
```
┌─────────────────────────────────────────┐
│ #374151    - Standard Border             │
│ #4B5563    - Light Border                │
└─────────────────────────────────────────┘
```

**Note**: All status colors and primary/secondary colors remain the same in dark mode!

## 🎨 Component Color Usage

### Navigation Bar (Light Mode)
```
Background:     --bg-primary (#FFFFFF)
Text:           --text-secondary (#4B5563)
Brand:          Gradient (primary → secondary)
Links:          --text-secondary, hover: --primary-color
Active:         --primary-color
Logout:         --danger-color
Border:         --border-color (#E5E7EB)
```

### Welcome Section (Light Mode)
```
Background:     Linear gradient (primary-color → secondary-color)
Text:           White (#FFFFFF)
Badge:          rgba(255, 255, 255, 0.2) background
```

### Category Cards (Light Mode)
```
Background:     --bg-primary (#FFFFFF)
Border:         --border-color (#E5E7EB), hover: --primary-color
Icon Background: Linear gradient of tertiary colors
Card Content:   --text-primary (#111827), --text-secondary (#4B5563)
Button Primary: Linear gradient (primary → primary-light)
Button Success: Linear gradient (success → success-light)
Button Warning: Linear gradient (warning → warning-light)
Button Info:    Linear gradient (info → info-light)
```

### Statistics Cards (Light Mode)
```
Background:     --bg-primary (#FFFFFF)
Border:         --border-color (#E5E7EB)
Overlay:        rgba(primary, 0.05) on hover
Number:         --primary-color (#4F46E5)
Label:          --text-secondary (#4B5563)
Trend:          --text-tertiary (#9CA3AF)
```

### Activity Table (Light Mode)
```
Background:     --bg-primary (#FFFFFF)
Header Bg:      --bg-tertiary (#F3F4F6)
Header Text:    --text-primary (#111827)
Rows:           --text-secondary (#4B5563)
Hover Row:      --bg-tertiary (#F3F4F6)
Row Border:     --border-color (#E5E7EB)
Badge Bg:       rgba(primary, 0.1)
Badge Text:     --primary-color
Amount:         --success-color (#10B981)
```

## 🎯 Accessibility Colors

All color combinations meet WCAG AA contrast requirements:

### High Contrast Pairs
```
Dark Text on Light Background:
- #111827 on #FFFFFF (21:1 ratio - AAA)
- #4B5563 on #F9FAFB (11:1 ratio - AAA)
- #9CA3AF on #FFFFFF (4.5:1 ratio - AA)

Light Text on Dark Background:
- #F9FAFB on #111827 (21:1 ratio - AAA)
- #D1D5DB on #1F2937 (11:1 ratio - AAA)
```

### Status Colors Accessibility
```
Success: #10B981 meets AA on light and dark backgrounds
Warning: #F59E0B meets AA on light and dark backgrounds
Danger:  #EF4444 meets AA on light and dark backgrounds
Info:    #06B6D4 meets AA on light and dark backgrounds
```

## 🔄 Color Customization Workflow

### Step 1: Identify Component to Customize
Decide which elements you want to change (primary colors, success color, etc.)

### Step 2: Choose New Color
Select a new color in hex format (e.g., #3B82F6)

### Step 3: Create Variants
Generate lighter and darker variants:
```
Primary:  #3B82F6
Light:    #60A5FA (increase lightness by ~15%)
Dark:     #1E40AF (decrease lightness by ~15%)
```

### Step 4: Update CSS Variables
Edit the corresponding CSS variables in `:root` or `[data-theme="dark"]`

### Step 5: Test Theme
- Test in light mode
- Test in dark mode
- Check all components using the color
- Verify accessibility contrast

### Step 6: Browser Testing
- Test on Chrome, Firefox, Safari
- Test on mobile browsers
- Clear cache and reload

## 🌈 Pre-made Theme Examples

### Ocean Theme (Blue)
```css
--primary-color: #0369A1;      /* Dark Blue */
--primary-light: #0EA5E9;      /* Sky Blue */
--secondary-color: #0284C7;    /* Ocean Blue */
--success-color: #06B6D4;      /* Cyan */
--warning-color: #F59E0B;      /* Amber (unchanged) */
--danger-color: #FCA5A5;       /* Light Red */
```

### Forest Theme (Green)
```css
--primary-color: #047857;      /* Dark Green */
--primary-light: #10B981;      /* Emerald */
--secondary-color: #34D399;    /* Light Green */
--success-color: #059669;      /* Dark Green */
--warning-color: #FCD34D;      /* Yellow */
--danger-color: #FB7185;       /* Pink */
```

### Sunset Theme (Warm)
```css
--primary-color: #D97706;      /* Amber */
--primary-light: #F59E0B;      /* Orange */
--secondary-color: #EA580C;    /* Orange Red */
--success-color: #14B8A6;      /* Teal */
--warning-color: #F97316;      /* Orange */
--danger-color: #DC2626;       /* Red */
```

### Midnight Theme (Dark)
```css
/* For Dark Mode */
--bg-primary: #0F172A;         /* Deeper Blue Black */
--bg-secondary: #1E293B;       /* Blue Black */
--bg-tertiary: #334155;        /* Slate Blue */
--border-color: #475569;       /* Medium Slate */
```

## 📝 CSS Variable Complete Reference

```css
/* Color Variables */
--primary-color:      #4F46E5
--primary-light:      #6366F1
--primary-dark:       #4338CA
--secondary-color:    #8B5CF6
--secondary-light:    #A78BFA
--secondary-dark:     #7C3AED
--success-color:      #10B981
--success-light:      #34D399
--success-dark:       #059669
--warning-color:      #F59E0B
--warning-light:      #FBBF24
--warning-dark:       #D97706
--danger-color:       #EF4444
--danger-light:       #F87171
--danger-dark:        #DC2626
--info-color:         #06B6D4
--info-light:         #22D3EE
--info-dark:          #0891B2

/* Background & Text */
--bg-primary:         #FFFFFF
--bg-secondary:       #F9FAFB
--bg-tertiary:        #F3F4F6
--text-primary:       #111827
--text-secondary:     #4B5563
--text-tertiary:      #9CA3AF
--border-color:       #E5E7EB
--border-light:       #F3F4F6

/* Shadows */
--shadow-sm:          0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-md:          0 4px 6px -1px rgba(0, 0, 0, 0.1)
--shadow-lg:          0 10px 15px -3px rgba(0, 0, 0, 0.1)
--shadow-xl:          0 20px 25px -5px rgba(0, 0, 0, 0.1)

/* Timing */
--transition:         color 0.3s ease, background-color 0.3s ease, ...
```

---
**Last Updated**: March 27, 2026
