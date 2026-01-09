# Project Constitution: Desktop Snow Overlay

## 1. Tech Stack
- **Language:** Python 3.10+
- **GUI Framework:** PyQt6 (Qt Widgets)
- **Dependency Manager:** `pip` (use `venv`)

## 2. Core Architecture Rules (Hard Constraints)
- **Click-Through:** Окно должно быть абсолютно прозрачным для событий мыши. Я должен иметь возможность кликать сквозь снег по иконкам на рабочем столе.
- **Always On Top:** Окно снега должно быть поверх всех окон.
- **Tray Icon:** Так как окно не ловит клики, у приложения ОБЯЗАТЕЛЬНО должна быть иконка в системном трее (System Tray) с кнопкой "Exit" для закрытия.
- **Performance:** Используй `QTimer` для анимации. Не блокируй GUI-поток `time.sleep()`.

## 3. Code Style
- Используй Type Hints (typing).
- Логику частиц (Snowflakes) выноси в отдельный класс.
- Никаких `try-catch` без логирования.