from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QScreen, QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication

from .snowflake import Snowflake
from .config import config


class ExitButtonWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.geometry()
            self.setGeometry(10, screen_geometry.height() - 50, 50, 40)

        self.exit_button = QPushButton("✕", self)
        self.exit_button.setFixedSize(30, 30)
        self.exit_button.clicked.connect(self.exit_app)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(255, 255, 255, 150);
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 220);
                color: white;
            }
        """)

        self.show()

    def exit_app(self):
        QApplication.quit()


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.geometry()
            self.setGeometry(screen_geometry)

        self.snowflakes = []
        self.frame_count = 0
        self.init_snowflakes()
        print(f"[OverlayWindow] Created {len(self.snowflakes)} snowflakes")

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(1000 // config.FPS)

        QWidget.show(self)
        print(f"[OverlayWindow] Window shown, visible: {self.isVisible()}")

        exit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        exit_shortcut.activated.connect(self.exit_app)

        escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        escape_shortcut.activated.connect(self.exit_app)

        print("[OverlayWindow] Hotkeys: Ctrl+Q or Escape to exit")

        self.exit_button_window = ExitButtonWindow(self)

    def init_snowflakes(self):
        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.geometry()
            for _ in range(config.SNOW_COUNT):
                self.snowflakes.append(
                    Snowflake(screen_geometry.width(), screen_geometry.height())
                )

    def animate(self):
        time_delta = 1.0
        for snowflake in self.snowflakes:
            snowflake.update(time_delta, self.frame_count)
        self.frame_count += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for snowflake in self.snowflakes:
            color = QColor(200, 230, 255, int(255 * snowflake.opacity))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(
                QPointF(snowflake.x, snowflake.y), snowflake.size, snowflake.size
            )

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.exit_button_window.hide()
        else:
            self.show()
            self.exit_button_window.show()

    def exit_app(self):
        self.timer.stop()
        QApplication.quit()

    def close(self):
        self.timer.stop()
        return super().close()
