"""
MarkdownViewer widget for rendering markdown in the Kivy GUI.

This widget will be used to display the research report in a "pretty" state.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

try:
    from kivymd.uix.label import MDLabel
    from kivymd.uix.card import MDCard
    from kivy_garden.markdown import MarkdownLabel
except ImportError:
    MarkdownLabel = None  # Placeholder if not installed

class MarkdownViewer(BoxLayout):
    markdown_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        if MarkdownLabel:
            self.markdown_widget = MarkdownLabel(text=self.markdown_text)
            self.add_widget(self.markdown_widget)
        else:
            self.add_widget(
                MDLabel(text="Markdown rendering not available. Install kivy_garden.markdown.", halign="left")
            )

    def on_markdown_text(self, instance, value):
        if MarkdownLabel:
            self.markdown_widget.text = value