import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
print("DEBUG sys.path (patched):", sys.path)
print("DEBUG os.getcwd():", os.getcwd())
import sys, os
print("DEBUG sys.path:", sys.path)
print("DEBUG os.getcwd():", os.getcwd())
"""
Unit tests for the main Kivy GUI app.
"""

import pytest
from kivy.base import EventLoop
from kivy.config import Config

# Ensure Kivy does not open a window during tests
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'width', '800')

from gui.main import ResearchAgentApp

@pytest.fixture(scope="module")
def app():
    EventLoop.ensure_window()
    app = ResearchAgentApp()
    return app

def test_app_builds(app):
    root = app.build()
    assert root is not None
    assert hasattr(root, 'ids')
    assert 'topic_input' in root.ids
    assert 'markdown_output' in root.ids
    assert 'status_panel' in root.ids

def test_clear_button(app):
    root = app.build()
    root.ids.topic_input.text = "Test topic"
    root.ids.markdown_output.text = "Some output"
    root.ids.status_panel.text = "Status: Running"
    app.root = root  # Patch: set app.root for handler to work
    app.on_clear()
    assert root.ids.topic_input.text == ""
    assert root.ids.markdown_output.text == ""
    assert root.ids.status_panel.text == "Status: Idle"