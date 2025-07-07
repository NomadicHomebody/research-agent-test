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

class DummyMDApp(MDApp):
    def build(self):
        return None

@pytest.fixture(scope="module", autouse=True)
def setup_kivy():
    EventLoop.ensure_window()
    if not MDApp.get_running_app():
        DummyMDApp().run()  # Start and immediately stop a dummy MDApp

def test_markdown_viewer_initializes():
    # Skip test if kivy_garden.markdown is not installed (avoids KivyMD fallback error)
    from gui.widgets.markdown_viewer import MarkdownLabel
    import pytest
    if MarkdownLabel is None:
        pytest.skip("kivy_garden.markdown not installed; skipping MarkdownViewer test.")
    widget = MarkdownViewer()
    assert hasattr(widget, "markdown_text")
    # Should have at least one child (the markdown label or fallback)
    assert len(widget.children) > 0

def test_status_panel_updates():
    panel = StatusPanel()
    assert panel.status_text == "Status: Idle"
    panel.set_status("Status: Running")
    assert panel.status_text == "Status: Running"

def test_dynamic_background_color_changes():
    bg = DynamicBackground()
    # Simulate mouse at center
    w, h = 800, 600
    bg.on_mouse_pos(None, (w // 2, h // 2))
    r, g, b = bg.bg_color.r, bg.bg_color.g, bg.bg_color.b
    assert 0.1 <= r <= 0.6
    assert 0.1 <= g <= 0.6
    assert 0.15 <= b <= 0.65