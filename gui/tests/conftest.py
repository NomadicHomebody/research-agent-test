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