"""
StatusPanel widget for displaying agent status and icons in the Kivy GUI.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class StatusPanel(BoxLayout):
    status_text = StringProperty("Status: Idle")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        # Placeholder for icon/image support
        # You can add an Image widget for status icons here

    def set_status(self, text: str):
        """Update the status text."""
        self.status_text = text