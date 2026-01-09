# Snow Overlay — Implementation Plan

## Overview
Create a click-through snow overlay application using PyQt6 that displays falling snowflakes on screen without blocking mouse interactions.

## Architecture

### Core Components
```
Snow Overlay Application
├── OverlayWindow (Main transparent window)
│   ├── QWidget as base
│   ├── Custom painting via QPainter
│   └── Snowflake management
├── Snowflake (Data class for individual flakes)
│   ├── Position (x, y)
│   ├── Size (radius)
│   ├── Velocity (fall speed, sway)
│   └── Opacity/alpha
└── TrayIcon (System tray management)
    ├── QSystemTrayIcon
    ├── Context menu (Show/Hide, Exit)
    └── Toggle visibility
```

## Implementation Steps

### Step 1: Project Structure Setup
```
snow_overlay/
├── main.py              # Entry point
├── snow_overlay/
│   ├── __init__.py
│   ├── overlay_window.py  # OverlayWindow class
│   ├── snowflake.py       # Snowflake class
│   ├── tray_icon.py       # TrayIcon class
│   └── config.py          # Configuration constants
├── docs/
│   └── plan.md           # This file
└── requirements.txt
```

### Step 2: Snowflake Class
**File:** `snowflake.py`

```python
class Snowflake:
    def __init__(self, screen_width, screen_height):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(-screen_height, 0)
        self.size = random.uniform(1.0, 4.0)  # Random radius
        self.fall_speed = random.uniform(1.0, 3.0)  # Vertical velocity
        self.sway_amplitude = random.uniform(0.5, 2.0)  # Horizontal sway
        self.sway_frequency = random.uniform(0.02, 0.05)  # Sway speed
        self.sway_offset = random.uniform(0, 2 * math.pi)  # Random phase
        self.opacity = random.uniform(0.4, 0.9)

    def update(self, time_delta):
        self.y += self.fall_speed * time_delta
        self.x += math.sin(time_delta * self.sway_frequency + self.sway_offset) * self.sway_amplitude

    def reset(self, screen_width, screen_height):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(-screen_height, 0)
```

### Step 3: OverlayWindow Class
**File:** `overlay_window.py`

**Critical Window Setup (from overlay-setup skill):**
```python
def __init__(self):
    super().__init__()

    # Window flags for click-through overlay
    self.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool
    )

    # Transparent background
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # Click-through (mouse events pass through)
    self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    # Full screen
    screen_geometry = QApplication.primaryScreen().geometry()
    self.setGeometry(screen_geometry)

    # Initialize snowflakes
    self.snowflakes = []
    self.snow_count = 500  # Configurable
    self.init_snowflakes()
```

**Painting Logic:**
- Override `paintEvent()` to draw snowflakes
- Use QPainter with composition mode for smooth edges
- Draw each snowflake as an ellipse with varying opacity

**Animation:**
- Use QTimer for animation loop (60 FPS target)
- Update snowflake positions each frame
- Reset snowflakes that fall below screen

### Step 4: TrayIcon Class
**File:** `tray_icon.py`

```python
class TrayIcon:
    def __init__(self, overlay_window):
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("snowflake.png"))

        # Context menu
        self.menu = QMenu()
        show_action = self.menu.addAction("Show/Hide")
        exit_action = self.menu.addAction("Exit")

        show_action.triggered.connect(overlay_window.toggle_visibility)
        exit_action.triggered.connect(overlay_window.close)

        self.tray.setContextMenu(self.menu)
        self.tray.show()
```

### Step 5: Main Entry Point
**File:** `main.py`

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)

    overlay = OverlayWindow()
    tray = TrayIcon(overlay)

    sys.exit(app.exec())
```

## Configuration Options (config.py)
```python
SNOW_COUNT = 500
MIN_SIZE = 1.0
MAX_SIZE = 4.0
MIN_SPEED = 1.0
MAX_SPEED = 3.0
SWAY_AMPLITUDE = 0.5, 2.0
FPS = 60
```

## Physics Details

### Sway Motion
Snowflakes don't fall straight down. Use sinusoidal motion:
```
x(t) = x0 + A * sin(ω * t + φ)
```
Where:
- A = sway_amplitude (random per flake)
- ω = sway_frequency (random per flake)
- φ = sway_offset (random per flake)
- t = time or frame counter

### Random Distribution
- Use `random.uniform()` for continuous values
- All snowflakes should have slightly different parameters to avoid uniform appearance
- Consider using Gaussian distribution for more natural look

## Dependencies
```
PyQt6>=6.6.0
```

## Testing Checklist
- [ ] Window appears on top of all applications
- [ ] Mouse clicks pass through to underlying apps
- [ ] Snowflakes animate smoothly
- [ ] Snowflakes reset at top after falling off screen
- [ ] Tray icon appears in system tray
- [ ] Show/Hide menu item toggles visibility
- [ ] Exit menu item closes application
- [ ] Application starts minimized to tray (optional)

## Key Implementation Notes
1. Always use `WA_TransparentForMouseEvents` for click-through functionality
2. Use `WA_TranslucentBackground` with `FramelessWindowHint` for transparent background
3. `Tool` flag prevents window from appearing in taskbar
4. Animation must be efficient (avoid heavy operations in paintEvent)
5. Consider performance with 500+ snowflakes - test on lower-end hardware
