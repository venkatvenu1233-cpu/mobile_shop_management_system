# Developer Quick Reference - Dashboard Theme System

## 🔧 At a Glance

**CSS File**: `static/dashboard-theme.css` (1000+ lines)
**HTML File**: `templates/user/dashboard.html` (Updated)
**Theme Toggle**: Built-in (☀️/🌙 button)
**Variables**: 30+ CSS custom properties
**Themes**: 8 pre-made + unlimited custom

---

## 🎨 CSS Variables Quick List

### Status Colors
```css
--primary-color: #4F46E5;      --primary-light: #6366F1;      --primary-dark: #4338CA;
--success-color: #10B981;      --success-light: #34D399;      --success-dark: #059669;
--warning-color: #F59E0B;      --warning-light: #FBBF24;      --warning-dark: #D97706;
--danger-color: #EF4444;       --danger-light: #F87171;       --danger-dark: #DC2626;
--info-color: #06B6D4;         --info-light: #22D3EE;         --info-dark: #0891B2;
```

### Background & Text
```css
--bg-primary: #FFFFFF;         --bg-secondary: #F9FAFB;       --bg-tertiary: #F3F4F6;
--text-primary: #111827;       --text-secondary: #4B5563;     --text-tertiary: #9CA3AF;
--border-color: #E5E7EB;       --border-light: #F3F4F6;
```

### Dark Mode
```css
[data-theme="dark"] {
    --bg-primary: #111827;     --bg-secondary: #1F2937;       --bg-tertiary: #374151;
    --text-primary: #F9FAFB;   --text-secondary: #D1D5DB;     --border-color: #374151;
}
```

---

## 🔍 CSS Structure

```
dashboard-theme.css
├── Lines 1-7:      License & Header Comments
├── Lines 8-63:     CSS Variables & Themes
├── Lines 64-200:   Global Styles & Typography
├── Lines 201-300:  Theme Toggle Button
├── Lines 301-450:  Navigation Bar
├── Lines 451-550:  Container & Layout
├── Lines 551-700:  Welcome Section
├── Lines 701-900:  Category Cards
├── Lines 901-1050: Statistics
├── Lines 1051-1200: Activity Table
└── Lines 1201+:    Responsive & Print Styles
```

---

## 🎯 Common Code Snippets

### Change All Primary Colors
```css
:root {
    --primary-color: #0056B3;      /* Changed from #4F46E5 */
    --primary-light: #0069D9;      /* Changed from #6366F1 */
    --primary-dark: #003D82;       /* Changed from #4338CA */
}
```

### Change Dark Mode Background
```css
[data-theme="dark"] {
    --bg-primary: #0A1929;         /* Changed from #111827 */
    --bg-secondary: #132F4C;       /* Changed from #1F2937 */
    --bg-tertiary: #1A3A52;        /* Changed from #374151 */
}
```

### Custom Button Style
```css
.custom-button {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    transition: var(--transition);
}

.custom-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
```

### Apply Theme to New Component
```css
.my-component {
    background: var(--bg-primary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
    transition: var(--transition);
}

.my-component:hover {
    box-shadow: var(--shadow-lg);
}
```

---

## 🎬 Animation Reference

### Available Animations
```css
@keyframes float { }           /* Floating effect */
@keyframes fadeIn { }          /* Fade in effect */
@keyframes slideInDown { }     /* Slide down */
@keyframes pulse-circle { }    /* Pulse circle */
@keyframes spin-slow { }       /* Slow rotation */
@keyframes shimmer { }         /* Shimmer effect */
```

### Usage
```css
animation: float 3s ease-in-out infinite;
animation: fadeIn 0.5s ease-out;
animation: spin-slow 20s linear infinite;
```

---

## 📱 Responsive Breakpoints

```css
/* Desktop */
@media (max-width: 1024px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Mobile */
@media (max-width: 480px) { }
```

---

## 🎓 CSS Classes Reference

### Container & Layout
```css
.container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
.theme-toggle-container { position: fixed; top: 20px; right: 20px; }
.navbar { position: sticky; top: 0; }
```

### Theme Toggle
```css
.theme-toggle { }
.theme-toggle:hover { transform: scale(1.1) rotate(20deg); }
.sun-icon { }
.moon-icon { }
[data-theme="dark"] .sun-icon { opacity: 0; }
[data-theme="dark"] .moon-icon { opacity: 1; }
```

### Navigation
```css
.navbar { }
.nav-container { display: flex; }
.nav-brand { display: flex; gap: 1rem; }
.nav-link { text-decoration: none; position: relative; }
.nav-link::after { content: ''; width: 0; transition: width 0.3s ease; }
.nav-link:hover::after { width: 100%; }
```

### Content Sections
```css
.welcome-section { background: linear-gradient(...); }
.category-card { }
.category-card:hover { transform: translateY(-8px); }
.category-icon { }
.category-content { }
.stats-section { }
.stat-card { }
.recent-activity-section { }
```

### Table
```css
.activity-table { width: 100%; }
.activity-table th { background: var(--bg-tertiary); }
.activity-table td { border-bottom: 1px solid var(--border-color); }
.table-row:hover { background-color: var(--bg-tertiary); }
.quantity-badge { }
.date-badge { }
.empty-state { }
```

---

## 🔌 JavaScript Integration

### Theme Toggle
```javascript
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Get current theme from localStorage
const currentTheme = localStorage.getItem('theme') || 'light';
htmlElement.setAttribute('data-theme', currentTheme);

// Toggle theme on button click
themeToggle.addEventListener('click', () => {
    const newTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});
```

### Theme Detection
```javascript
// Check current theme
const currentTheme = document.documentElement.getAttribute('data-theme');

// Dark mode check
const isDarkMode = currentTheme === 'dark';

// Watch for theme changes
const observer = new MutationObserver(() => {
    const newTheme = document.documentElement.getAttribute('data-theme');
    console.log('Theme changed to:', newTheme);
});

observer.observe(document.documentElement, { attributes: true });
```

---

## 🔍 Debugging Tips

### Check Current Theme
```javascript
// In browser console
document.documentElement.getAttribute('data-theme')
// Returns: 'light' or 'dark'
```

### Check CSS Variables
```javascript
// In browser console
getComputedStyle(document.documentElement)
    .getPropertyValue('--primary-color')
// Returns: '#4F46E5'
```

### Inspect Applied Styles
```javascript
// In browser console
window.getComputedStyle(document.querySelector('.stat-card'))
// Returns all computed styles
```

### Clear Theme
```javascript
// In browser console
localStorage.removeItem('theme')
// Clears saved theme preference
```

---

## 📊 Colors by Component

### Navigation
| Element | Color Variable | Used For |
|---------||---|
| Background | --bg-primary | Container |
| Text | --text-secondary | Links |
| Active Link | --primary-color | Current page |
| Logout | --danger-color | Danger action |

### Buttons
| Type | Background | Text |
|------|-----------|------|
| Primary | --primary to --primary-light gradient | White |
| Success | --success color | White |
| Warning | --warning color | White |
| Danger | --danger color | White |
| Info | --info color | White |

### Cards
| Element | Color Variable | Used For |
|---------|---|---|
| Background | --bg-primary | Card body |
| Border | --border-color | Card outline |
| Text | --text-primary | Title |
| Secondary Text | --text-secondary | Description |

---

## ⚡ Performance Tips

### CSS Optimization
- ✅ Variables reduce code duplication
- ✅ GPU-accelerated animations (transform, opacity)
- ✅ Minimal repaints (uses CSS transitions)
- ✅ No JavaScript overhead for styling

### Best Practices
```css
/* Good - Uses CSS variables */
.button {
    background: var(--primary-color);
    transition: var(--transition);
}

/* Good - GPU accelerated */
.button:hover {
    transform: translateY(-2px);
}

/* Avoid - Causes repaints */
.button:hover {
    width: 200px;  /* Avoid */
    height: 50px;  /* Avoid */
}
```

---

## 🧪 Testing Checklist

- [ ] Light mode renders correctly
- [ ] Dark mode renders correctly
- [ ] Theme toggle switches properly
- [ ] Theme persists after refresh
- [ ] Responsive on desktop (1024px+)
- [ ] Responsive on tablet (768px-1023px)
- [ ] Responsive on mobile (480px-767px)
- [ ] Responsive on small mobile (<480px)
- [ ] All colors have sufficient contrast
- [ ] Animations are smooth
- [ ] No console errors
- [ ] Page loads quickly

---

## 📦 Integration Steps

### Step 1: Link CSS
```html
<link rel="stylesheet" href="{{ url_for('static', filename='dashboard-theme.css') }}">
```

### Step 2: Add Toggle Button
```html
<div class="theme-toggle-container">
    <button class="theme-toggle" id="themeToggle">
        <svg class="sun-icon">...</svg>
        <svg class="moon-icon">...</svg>
    </button>
</div>
```

### Step 3: Add JavaScript
```html
<script>
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-theme', currentTheme);
    
    themeToggle.addEventListener('click', () => {
        const newTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
</script>
```

---

## 🚀 Advanced Customization

### Create New Theme Variant
```css
[data-theme="blue"] {
    --primary-color: #0056B3;
    --primary-light: #0069D9;
    --primary-dark: #003D82;
    --bg-primary: #F0F4F8;
    /* ... other variables */
}
```

### Add Custom Font
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
}
```

### Add Custom Animation
```css
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.element {
    animation: slideUp 0.3s ease-out;
}
```

---

## 📖 File Paths

| File | Path | Purpose |
|------|------|---------|
| Main CSS | `static/dashboard-theme.css` | Theme CSS |
| Dashboard HTML | `templates/user/dashboard.html` | Dashboard page |
| Original CSS | `static/style.css` | Preserved original |

---

## 🔗 Related Files

```
dashboard-theme.css
├── Variables (lines 8-63)
├── Global Styles (lines 64-200)
├── Navigation (lines 301-450)
├── Cards (lines 701-900)
├── Statistics (lines 901-1050)
├── Table (lines 1051-1200)
└── Responsive (lines 1201+)
```

---

## 💡 Quick Wins

1. **Change color in 30 seconds**: Edit CSS variable in `:root`
2. **Add new theme in 2 minutes**: Copy `:root` to `[data-theme="name"]`
3. **Speed up animations**: Reduce animation duration values
4. **Add new component**: Copy card structure, update class names

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Colors not applying | Clear cache, check syntax |
| Dark mode not working | Check `[data-theme="dark"]` exists |
| Animations laggy | Use transform/opacity only |
| Layout broken | Check responsive breakpoints |
| Icons missing | Verify SVG code in HTML |

---

## 📞 Quick Help

**CSS Variables not working?**
→ Check `:root` section syntax (colons, semicolons)

**Theme toggle broken?**
→ Check JavaScript in dashboard.html line 180+

**Colors wrong?**
→ Verify hex format (#RRGGBB) and contrast

**Layout issues?**
→ Check responsive breakpoints for your screen size

---

**Last Updated**: March 27, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
