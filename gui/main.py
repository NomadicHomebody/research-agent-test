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
import threading
import os

# Register custom widgets for KV loading
from .widgets.dynamic_background import DynamicBackground
from .widgets.markdown_viewer import MarkdownViewer
from .widgets.status_panel import StatusPanel

KV = '''
#:import Window kivy.core.window.Window

<MainLayout>:
    orientation: 'horizontal'
    DynamicBackground:
        id: bg
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.5
        padding: 20
        spacing: 10

        TextInput:
            id: topic_input
            hint_text: "Enter research topic..."
            size_hint_y: 0.6
            font_size: 20

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.15
            spacing: 10

            Button:
                id: submit_btn
                text: "Submit"
                # icon: 'icons/submit.svg'  # To be replaced with SVG icon
                on_release: app.on_submit()

            Button:
                id: clear_btn
                text: "Clear"
                # icon: 'icons/clear.svg'
                on_release: app.on_clear()

            Button:
                id: save_btn
                text: "Save"
                # icon: 'icons/save.svg'
                on_release: app.on_save()

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.25
            padding: [0, 20, 0, 0]
            Image:
                id: logo
                source: 'assets/logo.svg'
                size_hint_y: 0.7
            Label:
                text: "AI Research Agent"
                font_size: 18
                size_hint_y: 0.3
                halign: 'center'
                valign: 'middle'

    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.5
        padding: 20
        spacing: 10

        MarkdownViewer:
            id: markdown_viewer
            markdown_text: "Markdown output will appear here."
            size_hint_y: 0.8

        # StatusPanel:
        Label:
            id: status_panel
            text: "Status: Idle"
            font_size: 14
            size_hint_y: 0.2
            halign: 'left'
            valign: 'middle'
'''

class MainLayout(BoxLayout):
    pass

class ResearchAgentApp(MDApp):
    def build(self):
        print("DEBUG: Entered ResearchAgentApp.build()")
        print("DEBUG: KV string length:", len(KV))
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        Builder.load_string(KV)
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