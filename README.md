# Snow Overlay

A beautiful desktop snow effect that sits on top of all your windows without blocking mouse clicks. Built with PyQt6.

![Snow Overlay](docs/preview.png)

## Features

- **Click-through** - Mouse clicks pass through to underlying applications
- **System tray** - Minimize to tray with Show/Hide and Exit controls
- **Smooth animation** - 60 FPS with realistic snow physics
- **Customizable** - Easy to adjust snowflake count, speed, and appearance

## Installation

```bash
# Clone the repository
git clone https://github.com/arsen-ask-lx/snow-overlay.git
cd snow-overlay

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

- Look for the snowflake icon in your system tray
- Right-click for menu: Show/Hide Overlay, Exit
- Snowflakes fall smoothly on top of all windows

## Configuration

Edit `snow_overlay/config.py` to customize:

```python
SNOW_COUNT = 500          # Number of snowflakes
MIN_SIZE = 1.0            # Minimum flake size
MAX_SIZE = 4.0            # Maximum flake size
MIN_SPEED = 1.0           # Minimum fall speed
MAX_SPEED = 3.0           # Maximum fall speed
FPS = 60                  # Animation frames per second
```

## Architecture

```
snow_overlay/
├── __init__.py           # Package exports
├── config.py             # Configuration constants
├── snowflake.py          # Snowflake class with physics
├── overlay_window.py     # Click-through transparent window
└── tray_icon.py          # System tray management

.opencode/                # OpenCode agents and skills
├── agent/
│   └── architect.md      # Architecture planning agent
├── skill/
│   └── overlay-setup/    # Click-through overlay skill
└── AGENTS.md             # Agent configuration
```

## License

MIT
