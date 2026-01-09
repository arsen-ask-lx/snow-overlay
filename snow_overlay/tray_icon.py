from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor


def create_snowflake_icon():
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(255, 255, 255))
    painter.drawEllipse(16, 16, 8, 8)
    painter.end()

    return QIcon(pixmap)


class TrayIcon:
    def __init__(self, overlay_window):
        self.overlay_window = overlay_window
        self.tray = QSystemTrayIcon()

        icon = create_snowflake_icon()
        self.tray.setIcon(icon)
        print(f"[TrayIcon] Icon set, isValid: {not icon.isNull()}")

        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("[TrayIcon] WARNING: System tray is NOT available on this system!")
        else:
            print("[TrayIcon] System tray is available")

        self.menu = QMenu()

        self.show_action = QAction("Show/Hide Overlay")
        self.show_action.triggered.connect(overlay_window.toggle_visibility)
        self.menu.addAction(self.show_action)

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.show()
        print("[TrayIcon] Tray icon shown")

    def exit_app(self):
        self.overlay_window.close()
