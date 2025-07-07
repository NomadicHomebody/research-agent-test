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

import pytest
from kivymd.app import MDApp

@pytest.fixture
def app():
    # The MDApp context is provided by the session-scoped fixture in conftest.py
    return ResearchAgentApp()

def test_app_builds(app):
    root = app.build()
    assert root is not None
    assert hasattr(root, 'ids')
    assert 'topic_input' in root.ids
    assert 'markdown_viewer' in root.ids
    assert 'status_panel' in root.ids

def test_clear_button(app):
    root = app.build()
    root.ids.topic_input.text = "Test topic"
    root.ids.markdown_viewer.markdown_text = "Some output"
    root.ids.status_panel.text = "Status: Running"
    app.root = root  # Patch: set app.root for handler to work
    app.on_clear()
    assert root.ids.topic_input.text == ""
    assert root.ids.markdown_viewer.markdown_text == ""
    assert root.ids.status_panel.text == "Status: Idle"
import io
import tempfile
from unittest import mock

def test_load_markdown_report_success(app, tmp_path):
    # Create a valid markdown file
    md_path = tmp_path / "research_report.md"
    md_content = "# Test Report\n\nSome content."
    md_path.write_text(md_content, encoding="utf-8")
    with mock.patch("builtins.open", mock.mock_open(read_data=md_content)), \
         mock.patch("os.path.exists", return_value=True):
        app.root = app.build()
        app.root.ids.markdown_viewer.markdown_text = ""
        app.load_markdown_report()
        assert app.root.ids.markdown_viewer.markdown_text == md_content

def test_load_markdown_report_missing(app):
    with mock.patch("builtins.open", side_effect=FileNotFoundError):
        app.root = app.build()
        app.root.ids.markdown_viewer.markdown_text = ""
        app.load_markdown_report()
        assert "[Error] research_report.md not found." in app.root.ids.markdown_viewer.markdown_text

def test_load_markdown_report_empty(app):
    with mock.patch("builtins.open", mock.mock_open(read_data="")), \
         mock.patch("os.path.exists", return_value=True):
        app.root = app.build()
        app.root.ids.markdown_viewer.markdown_text = ""
        app.load_markdown_report()
        assert "empty" in app.root.ids.markdown_viewer.markdown_text or "Error" in app.root.ids.markdown_viewer.markdown_text

def test_load_markdown_report_malformed(app):
    malformed = "# Header\n\n*Unclosed italics"
    with mock.patch("builtins.open", mock.mock_open(read_data=malformed)), \
         mock.patch("os.path.exists", return_value=True):
        app.root = app.build()
        app.root.ids.markdown_viewer.markdown_text = ""
        app.load_markdown_report()
        # Should not raise, and text should match input or show error
        assert "Error" not in app.root.ids.markdown_viewer.markdown_text

def test_on_save_success(app, tmp_path):
    app.root = app.build()
    app.root.ids.markdown_viewer.markdown_text = "# Save Test"
    fake_file = tmp_path / "output.md"
    # Patch the filechooser import if it exists, otherwise skip the test
    try:
        import gui.main as main_mod
        filechooser = getattr(main_mod, "filechooser", None)
    except Exception:
        filechooser = None
    if filechooser is None:
        pytest.skip("filechooser not available in gui.main; skipping test_on_save_success.")
    with mock.patch.object(filechooser, "save_file") as mock_save_file:
        # Simulate filechooser callback
        def fake_callback(selection, *args, **kwargs):
            with open(fake_file, "w", encoding="utf-8") as f:
                f.write(app.root.ids.markdown_viewer.markdown_text)
            app.root.ids.status_panel.text = f"Status: Saved to {os.path.basename(fake_file)}"
        mock_save_file.side_effect = lambda **kwargs: kwargs["on_selection"]([str(fake_file)])
        app.on_save()
        assert fake_file.read_text(encoding="utf-8") == "# Save Test"
        assert "Saved to" in app.root.ids.status_panel.text

def test_on_save_cancel(app):
    app.root = app.build()
    try:
        import gui.main as main_mod
        filechooser = getattr(main_mod, "filechooser", None)
    except Exception:
        filechooser = None
    if filechooser is None:
        pytest.skip("filechooser not available in gui.main; skipping test_on_save_cancel.")
    with mock.patch.object(filechooser, "save_file") as mock_save_file:
        mock_save_file.side_effect = lambda **kwargs: kwargs["on_selection"]([])
        app.on_save()
        assert "Save cancelled" in app.root.ids.status_panel.text

def test_on_save_error(app):
    app.root = app.build()
    app.root.ids.markdown_viewer.markdown_text = "# Save Error"
    try:
        import gui.main as main_mod
        filechooser = getattr(main_mod, "filechooser", None)
    except Exception:
        filechooser = None
    if filechooser is None:
        pytest.skip("filechooser not available in gui.main; skipping test_on_save_error.")
    with mock.patch.object(filechooser, "save_file") as mock_save_file, \
         mock.patch("builtins.open", side_effect=IOError("Disk full")):
        def fake_callback(selection, *args, **kwargs):
            try:
                with open("fail.md", "w", encoding="utf-8") as f:
                    f.write(app.root.ids.markdown_viewer.markdown_text)
            except Exception:
                app.root.ids.status_panel.text = "Status: Error saving file - Disk full"
        mock_save_file.side_effect = lambda **kwargs: kwargs["on_selection"](["fail.md"])
        app.on_save()
        assert "Error saving file" in app.root.ids.status_panel.text