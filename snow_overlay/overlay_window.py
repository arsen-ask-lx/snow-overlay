from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QScreen, QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication

from .snowflake import Snowflake
from .config import config


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
        else:
            self.show()

    def exit_app(self):
        self.timer.stop()
        QApplication.quit()

    def close(self):
        self.timer.stop()
        return super().close()
