"""
Entry point for the Kivy-based GUI for the AI Research Agent.

This GUI provides:
- Responsive layout
- Text input for research topic
- SVG icon buttons (submit, clear, save)
- Status updates
- Markdown output rendering
- Dynamic background
- Modern theming

See ImplementationPlan.md section 8 for full requirements.
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.core.text import LabelBase
import threading
import os

# Register RobotoMono font for code blocks
try:
    LabelBase.register(name="RobotoMono", fn_regular=os.path.join(os.path.dirname(__file__), "assets", "RobotoMono.ttf"))
except Exception as e:
    print(f"WARNING: Could not register RobotoMono.ttf: {e}")

# Register custom widgets for KV loading
from gui.widgets.dynamic_background import DynamicBackground
from gui.widgets.markdown_viewer import MarkdownViewer
from gui.widgets.status_panel import StatusPanel

KV = '''
#:import Window kivy.core.window.Window
<MainLayout>:
    # Use FloatLayout for absolute positioning
    FloatLayout:
        DynamicBackground:
            id: bg
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}
            # Left column
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.5
                padding: 20
                spacing: 10

                TextInput:
                    id: topic_input
                    hint_text: "Enter research topic..."
                    size_hint_y: 0.5
                    font_size: 20
                    foreground_color: 0,0,0,1
                    background_color: 1,1,1,1
                    color: 0,0,0,1

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 0.15
                    spacing: 10

                    Button:
                        id: submit_btn
                        text: "Submit"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_submit()

                    Button:
                        id: clear_btn
                        text: "Clear"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_clear()

                    Button:
                        id: save_btn
                        text: "Save"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_save()

                StatusPanel:
                    id: status_panel
                    size_hint_y: 0.25

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 0.1
                    padding: [0, 10, 0, 0]
                    Label:
                        text: "AI Research Agent"
                        font_size: 18
                        size_hint_y: 1
                        halign: 'center'
                        valign: 'middle'
                        color: 0,0.12,0.3,1

            # Right column
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.5
                padding: 20
                spacing: 10

                MarkdownViewer:
                    id: markdown_viewer
                    markdown_text: "Markdown output will appear here."
                    size_hint_y: 0.8
'''
# Only load the KV string once at module import
from kivy.lang import Builder as _Builder
_Builder.load_string(KV)

class MainLayout(BoxLayout):
    """
    MainLayout is the root widget for the AI Research Agent GUI.

    - Left half: input, buttons, status panel, app label
    - Right half: markdown viewer
    - Uses DynamicBackground for visual effect
    """
    pass

class ResearchAgentApp(MDApp):
    """
    Main KivyMD application for the AI Research Agent.

    Handles:
    - Building the main layout and loading the KV string
    - Loading and displaying markdown reports
    - Handling submit, clear, and save actions
    - Updating status panel and markdown viewer
    """
    def build(self):
        print("DEBUG: Entered ResearchAgentApp.build()")
        print("DEBUG: KV string length:", len(KV))
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        return MainLayout()

    def load_markdown_report(self):
        """
        Loads the contents of research_report.md and sets it to the MarkdownViewer.
        Displays a user-friendly error if the file is missing or unreadable.
        """
        viewer = self.root.ids.markdown_viewer
        try:
            with open("research_report.md", "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                raise ValueError("Markdown file is empty.")
            viewer.markdown_text = content
        except FileNotFoundError:
            viewer.markdown_text = "[Error] research_report.md not found."
        except Exception as e:
            viewer.markdown_text = f"[Error] Could not load markdown: {str(e)}"

    def on_submit(self):
        topic = self.root.ids.topic_input.text.strip()
        if not topic:
            self.root.ids.status_panel.text = "Status: Please enter a research topic."
            return

        self.root.ids.status_panel.text = "Status: Running..."
        self.root.ids.markdown_viewer.markdown_text = "Running agent... (output will appear here)"

        def run_and_update():
            try:
                from agent_runner import run_agent
                run_agent(topic)
                if not os.path.exists("research_report.md"):
                    self.root.ids.status_panel.text = "Status: Error - research_report.md not found."
                    self.root.ids.markdown_viewer.markdown_text = "[Error] research_report.md not found."
                    return
                self.load_markdown_report()
                self.root.ids.status_panel.text = "Status: Complete"
            except Exception as e:
                self.root.ids.status_panel.text = f"Status: Error - {str(e)}"
                self.root.ids.markdown_viewer.markdown_text = f"[Error] Agent failed: {str(e)}"

        threading.Thread(target=run_and_update, daemon=True).start()

    def on_clear(self):
        self.root.ids.topic_input.text = ""
        self.root.ids.markdown_viewer.markdown_text = ""
        self.root.ids.status_panel.text = "Status: Idle"

    def on_save(self):
        """
        Opens a file save dialog and saves the current markdown report to the selected file.
        Provides user feedback via the status panel.
        """
        try:
            from kivy import platform
            if platform == "android":
                # On Android, filechooser is not available; show error
                self.root.ids.status_panel.text = "Status: Save not supported on Android."
                return
            from plyer import filechooser
        except ImportError:
            self.root.ids.status_panel.text = "Status: Save feature requires 'plyer' package."
            return

        def save_callback(selection):
            if not selection or not selection[0]:
                self.root.ids.status_panel.text = "Status: Save cancelled."
                return
            filepath = selection[0]
            text = self.root.ids.markdown_viewer.markdown_text
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                self.root.ids.status_panel.text = f"Status: Saved to {os.path.basename(filepath)}"
            except Exception as e:
                self.root.ids.status_panel.text = f"Status: Error saving file - {str(e)}"

        filechooser.save_file(title="Save Markdown Report", filters=[("Markdown files", "*.md"), ("All files", "*")], on_selection=save_callback)

if __name__ == "__main__":
    ResearchAgentApp().run()