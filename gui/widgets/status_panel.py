"""
StatusPanel widget for displaying agent status and icons in the Kivy GUI.
"""
# -----------------------------------------------------------------------------
# File: status_panel.py
# Location: test/gui/widgets/
#
# This widget displays the current status of the agent, including step progress,
# node name, and status messages, with modern styling and responsive layout.
#
# Used by: gui/main.py (as StatusPanel)
# Dependencies: Kivy (BoxLayout, Label, graphics), Kivy properties
# -----------------------------------------------------------------------------

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

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
    node_name = StringProperty("")
    progress = NumericProperty(0.0)
    total_steps = NumericProperty(0)
    current_step = NumericProperty(0)

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
            text=self._compose_status_text(),
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
        self.bind(node_name=self._on_status_update)
        self.bind(progress=self._on_status_update)
        self.bind(current_step=self._on_status_update)
        self.bind(total_steps=self._on_status_update)

        # Add canvas background for light grey
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.94, 0.94, 0.94, 1)  # #f0f0f0
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg, size=self._update_bg)

    def _on_status_text(self, instance, value):
        """Update label text when status_text changes."""
        self.label.text = self._compose_status_text()

    def _on_status_update(self, instance, value):
        """Update label text when any status property changes."""
        self.label.text = self._compose_status_text()

    def _compose_status_text(self) -> str:
        """Compose the full status text for display."""
        if self.node_name and self.total_steps > 0:
            return f"Step {self.current_step}/{self.total_steps}: {self.node_name} — {self.status_text}"
        elif self.node_name:
            return f"{self.node_name}: {self.status_text}"
        else:
            return self.status_text

    def _update_label_text_size(self, instance, value):
        """Ensure label text wraps and fills available space."""
        self.label.text_size = self.label.size

    def _update_bg(self, *args):
        """Update background rectangle position and size."""
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def set_status(self, text: str = None, node_name: str = None, current_step: int = None, total_steps: int = None):
        """
        Update the status panel with node-level details.

        Args:
            text (str): The new status message.
            node_name (str): The current node name.
            current_step (int): The current step number.
            total_steps (int): The total number of steps.
        """
        # Legacy mode: if only text is provided, reset node/progress
        if (
            text is not None
            and node_name is None
            and current_step is None
            and total_steps is None
        ):
            self.status_text = text
            self.node_name = ""
            self.current_step = 0
            self.total_steps = 0
        else:
            if text is not None:
                self.status_text = text
            if node_name is not None:
                self.node_name = node_name
            if current_step is not None:
                self.current_step = current_step
            if total_steps is not None:
                self.total_steps = total_steps
        # Compose label text
        self.label.text = self._compose_status_text()