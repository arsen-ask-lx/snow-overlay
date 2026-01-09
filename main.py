import sys
import time
from PyQt6.QtWidgets import QApplication

from snow_overlay.overlay_window import OverlayWindow
from snow_overlay.tray_icon import TrayIcon


def main():
    app = QApplication(sys.argv)

    overlay = OverlayWindow()
    tray = TrayIcon(overlay)

    print("[Snow Overlay] App started. Tray icon should appear in system tray.")
    print(f"[Snow Overlay] Window visible: {overlay.isVisible()}")
    print("[Snow Overlay] Check system tray for snowflake icon.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
