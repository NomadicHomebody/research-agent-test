"""
MarkdownViewer widget for rendering markdown in the Kivy GUI.

This widget will be used to display the research report in a "pretty" state.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

import markdown
from kivy.uix.label import Label

from kivymd.uix.label import MDLabel
from kivy.utils import get_color_from_hex

class MarkdownViewer(BoxLayout):
    """
    MarkdownViewer widget for rendering markdown as formatted rich text in the Kivy GUI.

    Features:
    - Converts markdown to Kivy markup for display using MDLabel
    - Handles lists, code blocks, bold, italics, etc.
    - Uses dark blue text for consistency with UI theme

    Args:
        markdown_text (str): Markdown content to render.
    """

    markdown_text = StringProperty("")

    def __init__(self, **kwargs):
        """
        Initialize the MarkdownViewer.

        Sets up the MDLabel for displaying formatted markdown,
        binds text updates, and ensures proper sizing.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.markdown_widget = MDLabel(
            text=self._render_markdown(self.markdown_text),
            halign="left",
            valign="top",
            markup=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#001f4d"),  # dark blue
            font_size=16,
        )
        self.markdown_widget.bind(size=self._update_text_size)
        self.add_widget(self.markdown_widget)

    def _update_text_size(self, instance, value):
        """Ensure label text wraps and fills available space."""
        self.markdown_widget.text_size = (self.markdown_widget.width, None)

    def on_markdown_text(self, instance, value):
        """
        Update the label when markdown_text changes.

        Args:
            instance: The property instance.
            value (str): The new markdown content.
        """
        self.markdown_widget.text = self._render_markdown(value)

    def _render_markdown(self, md_text):
        """
        Convert markdown to Kivy markup for display.

        Args:
            md_text (str): Markdown content.

        Returns:
            str: Kivy markup string.
        """
        html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
        # Simple HTML to Kivy markup conversion (limited)
        import re
        # Bold
        html = re.sub(r'<strong>(.*?)</strong>', r'[b]\1[/b]', html)
        # Italic
        html = re.sub(r'<em>(.*?)</em>', r'[i]\1[/i]', html)
        # Code blocks
        html = re.sub(r'<code>(.*?)</code>', r'[font=RobotoMono][color=#222222]\1[/color][/font]', html, flags=re.DOTALL)
        # Lists
        html = re.sub(r'<li>(.*?)</li>', r'• \1', html)
        # Remove other HTML tags
        html = re.sub(r'<[^>]+>', '', html)
        return html