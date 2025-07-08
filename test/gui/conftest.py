import pytest
from kivy.base import EventLoop
from kivymd.app import MDApp

class DummyMDApp(MDApp):
    def build(self):
        return None

import kivy
from kivymd.app import MDApp

@pytest.fixture(scope="session", autouse=True)
def mdapp_context():
    """
    Ensure a KivyMD App context is available for all tests.
    Initializes a DummyMDApp using _run_prepare() to avoid blocking the test runner.
    Monkeypatches App.get_running_app to always return the DummyMDApp instance.
    """
    if not EventLoop.event_listeners:
        EventLoop.ensure_window()
    if not MDApp.get_running_app():
        app = DummyMDApp()
        app._run_prepare()
        # Monkeypatch App.get_running_app to always return this MDApp
        MDApp.get_running_app = staticmethod(lambda: app)

# --- GLOBAL MOCKING OF EXTERNAL CALLS ---

from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_external_calls(monkeypatch):
    # Mock requests.get and requests.post
    import requests
    monkeypatch.setattr(requests, "get", MagicMock(return_value=MagicMock(status_code=200, content=b"mocked")))
    monkeypatch.setattr(requests, "post", MagicMock(return_value=MagicMock(status_code=200, content=b"mocked")))

    # Mock TavilySearchResults
    try:
        import research_graph
        monkeypatch.setattr(research_graph, "TavilySearchResults", MagicMock())
    except ImportError:
        pass

    # Mock GoogleGenerativeAI
    try:
        import langchain_google_genai
        monkeypatch.setattr(langchain_google_genai, "GoogleGenerativeAI", MagicMock())
    except ImportError:
        pass

    # Mock any other LLM/toolkit classes as needed
    # Add more mocks here if new external dependencies are added
