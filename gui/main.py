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
###############################################################################
# File Relationships and Architecture Overview
#
# - This file is the entry point for the Kivy-based GUI of the AI Research Agent.
# - It uses KivyMD for theming and Kivy for UI layout.
# - Custom widgets are imported from:
#     - test.gui.widgets.dynamic_background.DynamicBackground
#     - test.gui.widgets.markdown_viewer.MarkdownViewer
#     - test.gui.widgets.status_panel.StatusPanel
# - The GUI layout is defined in a KV string (see KV variable).
# - The left panel handles user input, action buttons, and status updates.
# - The right panel displays markdown output.
# - The app interacts with agent_runner.run_agent to execute research tasks.
# - File dialogs for loading/saving markdown use plyer.filechooser (desktop only).
# - The assets directory contains fonts and SVGs for UI styling.
#
# Dependencies:
#   - kivy, kivymd, plyer (for file dialogs), agent_runner (for agent execution)
#
# For a full requirements list, see ImplementationPlan.md section 8.
###############################################################################

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
                padding: [32, 32, 16, 32]
                spacing: 18

                TextInput:
                    id: topic_input
                    hint_text: "Enter research topic..."
                    size_hint_y: 0.45
                    font_size: 20
                    foreground_color: 0,0,0,1
                    background_color: 1,1,1,1
                    color: 0,0,0,1
                    padding: [12, 12, 12, 12]
                    multiline: False

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: 0.13
                    spacing: 14

                    Button:
                        id: submit_btn
                        text: "Submit"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_submit()
                        padding: [0, 8]
                        size_hint_x: 0.25

                    Button:
                        id: clear_btn
                        text: "Clear"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_clear()
                        padding: [0, 8]
                        size_hint_x: 0.25

                    Button:
                        id: save_btn
                        text: "Save"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_save()
                        padding: [0, 8]
                        size_hint_x: 0.25

                    Button:
                        id: load_btn
                        text: "Load"
                        background_color: 0,0.12,0.3,1
                        color: 1,1,1,1
                        font_size: 16
                        on_release: app.on_load()
                        padding: [0, 8]
                        size_hint_x: 0.25

                StatusPanel:
                    id: status_panel
                    size_hint_y: 0.25
                    background_color: 0.95,0.95,0.95,1
                    text_color: 0,0.12,0.3,1
                    padding: [10, 10, 10, 10]

            # Right column
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.5
                padding: [16, 32, 32, 32]
                spacing: 18

                MarkdownViewer:
                    id: markdown_viewer
                    markdown_text: "Markdown output will appear here."
                    size_hint_y: 1
                    padding: [10, 10, 10, 10]
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
    - Handling submit, clear, load, and save actions
    - Updating status panel and markdown viewer
    """
    
    def on_load(self):
        """
        Opens a file dialog to load a markdown file and displays its content in the MarkdownViewer.
        Handles errors and updates the status panel accordingly.
        """
        print("DEBUG: on_load called")
        try:
            from kivy import platform
            print(f"DEBUG: platform={platform}")
            if platform == "android":
                self.root.ids.status_panel.set_status("Status: Load not supported on Android.")
                print("DEBUG: Android platform detected, aborting load")
                return
            from plyer import filechooser
            print("DEBUG: plyer.filechooser import succeeded")
        except ImportError as e:
            self.root.ids.status_panel.set_status("Status: Load feature requires 'plyer' package.")
            print(f"DEBUG: ImportError in on_load: {e}")
            return

        def load_callback(selection):
            print(f"DEBUG: load_callback called with selection={selection}")
            if not selection or not selection[0]:
                self.root.ids.status_panel.set_status("Status: Load cancelled.")
                print("DEBUG: No file selected or selection empty")
                return
            filepath = selection[0]
            print(f"DEBUG: File selected: {filepath}")
            if not filepath.lower().endswith(".md"):
                self.root.ids.status_panel.set_status("Status: Please select a .md file.")
                print("DEBUG: Non-md file selected")
                return
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                if not content.strip():
                    self.root.ids.status_panel.set_status("Status: Selected file is empty.")
                    print("DEBUG: Selected file is empty")
                    return
                self.root.ids.markdown_viewer.markdown_text = content
                self.root.ids.status_panel.set_status(f"Status: Loaded {os.path.basename(filepath)}")
                print("DEBUG: Markdown loaded and displayed")
            except Exception as e:
                self.root.ids.status_panel.set_status(f"Status: Error loading file - {str(e)}")
                print(f"DEBUG: Exception loading file: {e}")

        print("DEBUG: Calling filechooser.open_file")
        filechooser.open_file(title="Load Markdown File", filters=[("Markdown files", "*.md")], on_selection=load_callback)
        print("DEBUG: filechooser.open_file call completed")

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
        """
        Handles the submit button click.

        Runs the agent in a background thread using threading.Thread.
        All UI updates (status panel and markdown viewer) are scheduled on the main thread
        using Kivy's Clock.schedule_once to ensure thread safety.

        Status transitions:
            - Idle → Running... (immediately on submit)
            - Running... → Complete (on success)
            - Running... → Error (on exception or missing output)

        Any exceptions in the agent thread are caught and reported to the UI.
        """
        from kivy.clock import Clock, mainthread

        topic = self.root.ids.topic_input.text.strip()
        status_panel = self.root.ids.status_panel
        markdown_viewer = self.root.ids.markdown_viewer

        if not topic:
            status_panel.set_status("Status: Please enter a research topic.")
            return

        status_panel.set_status("Status: Running...")
        markdown_viewer.markdown_text = "Running agent... (output will appear here)"

        def update_status(text):
            """Schedule status update on main thread."""
            status_panel.set_status(text)

        def update_markdown(text):
            """Schedule markdown update on main thread."""
            markdown_viewer.markdown_text = text

        def run_and_update():
            """
            Worker thread target for agent execution.
            All UI updates are scheduled on the main thread.
            """
            try:
                from agent_runner import run_agent
                from agent_runner import run_agent
                from kivy.clock import Clock

                def status_callback(node_name, status_message, current_step, total_steps):
                    def update_status_panel(dt):
                        status_panel.set_status(
                            text=status_message,
                            node_name=node_name,
                            current_step=current_step,
                            total_steps=total_steps
                        )
                    Clock.schedule_once(update_status_panel)

                run_agent(topic, status_callback=status_callback)
                if not os.path.exists("research_report.md"):
                    Clock.schedule_once(lambda dt: update_status("Status: Error - research_report.md not found."))
                    Clock.schedule_once(lambda dt: update_markdown("[Error] research_report.md not found."))
                    return
                # Load markdown and update status on main thread
                def finish_success(dt):
                    self.load_markdown_report()
                    status_panel.set_status("Status: Complete")
                Clock.schedule_once(finish_success)
            except Exception as e:
                Clock.schedule_once(lambda dt: update_status(f"Status: Error - {str(e)}"))
                Clock.schedule_once(lambda dt: update_markdown(f"[Error] Agent failed: {str(e)}"))

        threading.Thread(target=run_and_update, daemon=True).start()

    def on_clear(self):
        """
        Clears the input, output, and resets the status panel.
        """
        self.root.ids.topic_input.text = ""
        self.root.ids.markdown_viewer.markdown_text = ""
        self.root.ids.status_panel.set_status("Status: Idle")

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