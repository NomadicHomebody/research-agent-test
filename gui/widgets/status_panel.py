"""
StatusPanel widget for displaying agent status and icons in the Kivy GUI.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class StatusPanel(BoxLayout):
    """
    StatusPanel widget for displaying agent status with modern styling.

    Features:
    - Light grey background (#f0f0f0) using canvas
    - Dark blue text for status label
    - Stretches to fill parent BoxLayout
    - status_text property is bound to the label
    """

    status_text = StringProperty("Status: Idle")

    def __init__(self, **kwargs):
        """
        Initialize the StatusPanel.

        Adds a label bound to status_text, sets up background color,
        and ensures proper stretching and padding.
        """
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_x = 1
        self.size_hint_y = 1
        self.padding = [10, 10, 10, 10]
        self.spacing = 10

        from kivy.uix.label import Label
        self.label = Label(
            text=self.status_text,
            color=(0, 0.12, 0.3, 1),
            font_size=16,
            halign='left',
            valign='middle',
            size_hint=(1, 1)
        )
        self.label.bind(size=self._update_label_text_size)
        self.add_widget(self.label)

        # Bind status_text property to label text
        self.bind(status_text=self._on_status_text)

        # Add canvas background for light grey
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.94, 0.94, 0.94, 1)  # #f0f0f0
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg, size=self._update_bg)

    def _on_status_text(self, instance, value):
        """Update label text when status_text changes."""
        self.label.text = value

    def _update_label_text_size(self, instance, value):
        """Ensure label text wraps and fills available space."""
        self.label.text_size = self.label.size

    def _update_bg(self, *args):
        """Update background rectangle position and size."""
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def set_status(self, text: str):
        """
        Update the status text.

        Args:
            text (str): The new status message.
        """
        self.status_text = text