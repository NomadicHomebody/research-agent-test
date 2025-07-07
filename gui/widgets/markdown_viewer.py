"""
MarkdownViewer widget for rendering markdown in the Kivy GUI.

This widget will be used to display the research report in a "pretty" state.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

import markdown
from kivy.uix.label import Label

class MarkdownViewer(BoxLayout):
    markdown_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.markdown_widget = Label(text=self.markdown_text, halign="left", valign="top")
        self.markdown_widget.bind(size=self._update_text_size)
        self.add_widget(self.markdown_widget)

    def _update_text_size(self, instance, value):
        self.markdown_widget.text_size = (self.markdown_widget.width, None)

    def on_markdown_text(self, instance, value):
        # Render markdown as plain text (or optionally as HTML if a widget is available)
        # For now, just display the raw markdown
        self.markdown_widget.text = value