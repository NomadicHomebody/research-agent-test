"""
DynamicBackground widget for Kivy GUI.
Changes background color based on mouse position.
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class DynamicBackground(Widget):
    def __init__(self, **kwargs):
        # Ensure full window coverage
        kwargs.setdefault("size_hint", (1, 1))
        kwargs.setdefault("pos", (0, 0))
        super().__init__(**kwargs)
        with self.canvas:
            self.bg_color = Color(0.1, 0.1, 0.15, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=Window.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        Window.bind(mouse_pos=self.on_mouse_pos)
        # Robustly bind to Window size and position
        Window.bind(size=self._on_window_size)
        self._on_window_size(Window, Window.size)

    def _on_window_size(self, window, size):
        self.size = size
        self.pos = (0, 0)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_mouse_pos(self, window, pos):
        # Map mouse position to color gradient
        x, y = pos
        w, h = Window.size
        r = 0.1 + 0.5 * (x / w)
        g = 0.1 + 0.5 * (y / h)
        b = 0.15 + 0.5 * ((w - x) / w)
        self.bg_color.r = r
        self.bg_color.g = g
        self.bg_color.b = b