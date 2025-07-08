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

from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty
import logging

class CustomScrollView(ScrollView):
    """
    Custom ScrollView that disables OS/Kivy autoscroll by intercepting the middle mouse button.

    This prevents the default autoscroll mode (red circle) from being triggered when the user clicks
    the mouse wheel, ensuring normal scroll behavior is preserved in the MarkdownViewer.
    """
    def on_touch_down(self, touch):
        if 'button' in touch.profile and touch.button == 'middle':
            # Intercept middle mouse button to disable autoscroll
            return True  # Prevent default autoscroll
        return super().on_touch_down(touch)

class MarkdownViewer(BoxLayout):
    """
    MarkdownViewer widget for rendering markdown as formatted rich text in the Kivy GUI.

    Features:
    - Converts markdown to Kivy markup for display using MDLabel
    - Handles lists, code blocks, bold, italics, etc.
    - Uses dark blue text for consistency with UI theme
    - Egg-shell background (#F0EAD6)
    - Scrollable in both axes
    - Zoom in/out functionality

    Args:
        markdown_text (str): Markdown content to render.
    """

    markdown_text = StringProperty("")
    font_size = NumericProperty(16)
    _font_size_min = 10
    _font_size_max = 48

    def __init__(self, **kwargs):
        """
        Initialize the MarkdownViewer.

        Sets up the MDLabel for displaying formatted markdown,
        binds text updates, and ensures proper sizing.
        Also forcibly registers RobotoMono if not already registered.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*get_color_from_hex("#F0EAD6"))
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg_rect, size=self._update_bg_rect)

        # --- Force RobotoMono registration if not present ---
        from kivy.core.text import LabelBase
        if "RobotoMono" not in LabelBase._fonts:
            import os
            # Try to use a bundled font or fallback to system monospace
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "..", "assets", "RobotoMono-Regular.ttf"),
                os.path.join(os.path.dirname(__file__), "..", "..", "assets", "RobotoMono-Regular.ttf"),
                "/usr/share/fonts/truetype/roboto/RobotoMono-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "C:\\Windows\\Fonts\\consola.ttf",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    LabelBase.register(name="RobotoMono", fn_regular=path)
                    break

        # Use CustomScrollView to prevent OS/Kivy autoscroll (middle mouse) from interfering with normal scrolling.
        self.scroll_view = CustomScrollView(
            size_hint=(1, 1),
            bar_width=10,
            scroll_type=['bars', 'content'],
            do_scroll_x=True,
            do_scroll_y=True,
        )
        # MDLabel for displaying formatted markdown.
        # - size_hint_x=1: fills width of ScrollView viewport
        # - size_hint_y=None: height determined by content (texture_size[1])
        # - text_size: bound to ScrollView's width for proper wrapping
        self.markdown_widget = MDLabel(
            text=self._render_markdown(self.markdown_text),
            halign="left",
            valign="top",
            markup=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#001f4d"),  # dark blue
            font_size=self.font_size,
            size_hint=(1, None),  # Fill width, height set by content
        )
        # Bind label height to its texture height for vertical scrolling
        self.markdown_widget.bind(
            texture_size=self._update_label_height,
        )
        self.bind(font_size=self._on_font_size)
        # Bind ScrollView width to update label text_size for wrapping
        self.scroll_view.bind(width=self._update_label_text_size)
        self.scroll_view.add_widget(self.markdown_widget)
        self.add_widget(self.scroll_view)
        # Initial sizing
        self._update_label_text_size(self.scroll_view, self.scroll_view.width)
        self._update_label_height(self.markdown_widget, self.markdown_widget.texture_size)

    def _update_bg_rect(self, *args):
        if hasattr(self, "_bg_rect"):
            self._bg_rect.pos = self.pos
            self._bg_rect.size = self.size

    def _update_label_text_size(self, instance, width):
        """
        Update the label's text_size to match the ScrollView's viewport width.
        This ensures proper text wrapping and prevents horizontal scrolling.
        """
        # Subtract a small margin for scrollbar/padding if needed
        self.markdown_widget.text_size = (width, None)

    def _update_label_height(self, instance, texture_size):
        """
        Update the label's height to match its content (texture height).
        This enables vertical scrolling and prevents content clipping.
        """
        self.markdown_widget.height = texture_size[1]

    def on_markdown_text(self, instance, value):
        """
        Update the label when markdown_text changes.

        Args:
            instance: The property instance.
            value (str): The new markdown content.
        """
        self.markdown_widget.text = self._render_markdown(value)
        # Update label sizing after text change
        self._update_label_text_size(self.scroll_view, self.scroll_view.width)
        self._update_label_height(self.markdown_widget, self.markdown_widget.texture_size)

    def on_size(self, *args):
        # Ensure ScrollView resizes with parent
        if hasattr(self, "scroll_view"):
            self.scroll_view.size = self.size
        # Update label text_size for wrapping on resize
        self._update_label_text_size(self.scroll_view, self.scroll_view.width)

    def _on_font_size(self, instance, value):
        # Update label font size when property changes
        self.markdown_widget.font_size = value
        # Update label height after font size change
        self._update_label_height(self.markdown_widget, self.markdown_widget.texture_size)

    def zoom_in(self):
        """Increase font size, up to max."""
        if self.font_size < self._font_size_max:
            self.font_size += 2

    def zoom_out(self):
        """Decrease font size, down to min."""
        if self.font_size > self._font_size_min:
            self.font_size -= 2

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
        from kivy.core.text import LabelBase

        # Check if RobotoMono is registered (should always be after __init__)
        roboto_mono_registered = "RobotoMono" in LabelBase._fonts

        # Bold
        html = re.sub(r'<strong>(.*?)</strong>', r'[b]\1[/b]', html)
        # Italic
        html = re.sub(r'<em>(.*?)</em>', r'[i]\1[/i]', html)
        # Code blocks with fallback
        if roboto_mono_registered:
            html = re.sub(r'<code>(.*?)</code>', r'[font=RobotoMono][color=#222222]\1[/color][/font]', html, flags=re.DOTALL)
        else:
            html = re.sub(r'<code>(.*?)</code>', r'[color=#222222]\1[/color]', html, flags=re.DOTALL)
        # Lists
        html = re.sub(r'<li>(.*?)</li>', r'• \1', html)
        # Remove other HTML tags
        html = re.sub(r'<[^>]+>', '', html)
        return html

    def force_layout_update(self):
        """
        Force the label to update its texture and size.
        Useful for tests to ensure layout is correct before assertions.
        """
        self.markdown_widget.texture_update()
        self._update_label_height(self.markdown_widget, self.markdown_widget.texture_size)