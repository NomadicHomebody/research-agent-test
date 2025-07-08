import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
print("DEBUG sys.path (patched):", sys.path)
print("DEBUG os.getcwd():", os.getcwd())
import sys, os
print("DEBUG sys.path:", sys.path)
print("DEBUG os.getcwd():", os.getcwd())
"""
Unit tests for custom widgets in the Kivy GUI.
"""

import pytest
from kivy.base import EventLoop

from gui.widgets.markdown_viewer import MarkdownViewer
from gui.widgets.status_panel import StatusPanel
from gui.widgets.dynamic_background import DynamicBackground

# --- Patch: Provide a minimal MDApp context for KivyMD widgets ---
from kivymd.app import MDApp
# The MDApp context is provided by the session-scoped fixture in conftest.py

def test_markdown_viewer_initializes():
    viewer = MarkdownViewer()
    assert hasattr(viewer, "markdown_text")
    assert hasattr(viewer, "markdown_widget")
    assert len(viewer.children) > 0

def test_markdown_viewer_empty_markdown():
    viewer = MarkdownViewer()
    viewer.markdown_text = ""
    assert viewer.markdown_widget.text == ""

def test_markdown_viewer_malformed_markdown():
    viewer = MarkdownViewer()
    malformed = "# Header\n\n*Unclosed italics\n\n- List item\n- Another"
    viewer.markdown_text = malformed
    # Should render as formatted text (header, italics, list)
    assert "[b]Header[/b]" in viewer.markdown_widget.text or "Header" in viewer.markdown_widget.text
    assert "• List item" in viewer.markdown_widget.text

def test_markdown_viewer_renders_bold_italic_code():
    viewer = MarkdownViewer()
    md = "**bold** _italic_ `code`"
    viewer.markdown_text = md
    assert "[b]bold[/b]" in viewer.markdown_widget.text
    assert "[i]italic[/i]" in viewer.markdown_widget.text
    assert "[font=RobotoMono]" in viewer.markdown_widget.text

def test_markdown_viewer_large_markdown():
    viewer = MarkdownViewer()
    large_md = "# Title\n" + "\n".join([f"- Item {i}" for i in range(1000)])
    viewer.markdown_text = large_md
    assert "Item 999" in viewer.markdown_widget.text

def test_status_panel_updates():
    panel = StatusPanel()
    assert panel.status_text == "Status: Idle"
    panel.set_status("Status: Running")
    assert panel.status_text == "Status: Running"
    # Check label text and color
    assert hasattr(panel, "label")
    assert panel.label.text == "Status: Running"
    # Dark blue color
    assert tuple(panel.label.color) == (0, 0.12, 0.3, 1)
    # Check background color via canvas
    bg_color = None
    for instr in panel.canvas.before.children:
        if hasattr(instr, "rgba"):
            bg_color = instr.rgba
    assert bg_color is not None
    assert all(abs(a - b) < 0.01 for a, b in zip(bg_color, (0.94, 0.94, 0.94, 1)))

def test_dynamic_background_color_and_size(monkeypatch):
    from kivy.core.window import Window

    bg = DynamicBackground()
    # Simulate window size
    monkeypatch.setattr(Window, "size", (800, 600))
    # Simulate mouse at center
    w, h = Window.size
    bg.on_mouse_pos(None, (w // 2, h // 2))
    r, g, b = bg.bg_color.r, bg.bg_color.g, bg.bg_color.b
    assert 0.1 <= r <= 0.6
    assert 0.1 <= g <= 0.6
    assert 0.15 <= b <= 0.65

    # Assert background covers the full window
    assert tuple(bg.size) == tuple(Window.size)

def test_dynamic_background_stacking():
    """Ensure interactive widgets are above the background."""
    from kivy.uix.button import Button
    from kivy.uix.floatlayout import FloatLayout

    layout = FloatLayout()
    bg = DynamicBackground()
    btn = Button()
    layout.add_widget(bg)
    layout.add_widget(btn)
    # The last added widget should be on top
    assert layout.children[0] is btn
    assert layout.children[-1] is bg