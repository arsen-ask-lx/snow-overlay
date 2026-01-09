---
name: overlay-setup
description: Предоставляет правильные флаги окна для создания прозрачного Click-Through оверлея на PyQt6.
---

## Qt Window Flags for Click-Through Overlay

Когда создаешь главное окно (`QMainWindow` или `QWidget`), используй следующую конфигурацию в `__init__`:

```python
# Важно: Убираем рамки, держим поверх всех, делаем прозрачным фон
self.setWindowFlags(
    Qt.WindowType.FramelessWindowHint |
    Qt.WindowType.WindowStaysOnTopHint |
    Qt.WindowType.Tool  # Скрывает иконку из панели задач
)

# Важно: Делаем фон полностью прозрачным
self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

# CRITICAL: Пропуск кликов мыши (Click-Through)
self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

# Разворачиваем на весь экран
screen_geometry = QApplication.primaryScreen().geometry()
self.setGeometry(screen_geometry)


Используй этот шаблон всегда при инициализации окна.


---

### Шаг 3: Агент-Архитектор (`architect.md`)

Нам нужен тот, кто спланирует архитектуру частиц снега, не пытаясь сразу писать код.

**Создай папку:** `.opencode/agent/` (если нет)
**Файл:** `.opencode/agent/architect.md`

```yaml
---
description: Планирует архитектуру приложения, но не пишет код.
mode: primary
tools:
  edit: false
  bash: false
  skill: true
---

Ты — Senior GUI Architect. Твоя задача — составить план разработки оверлея.
Всегда проверяй `AGENTS.md` на наличие ограничений (Tray Icon, Click-Through).
Используй скилл `overlay-setup`, чтобы убедиться, что техническая реализация возможна.

Твой вывод — это файл плана (например, `docs/plan.md`).

