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

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

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

        # MarkdownViewer:
        Label:
            id: markdown_output
            text: "Markdown output will appear here."
            font_size: 16
            size_hint_y: 0.8
            text_size: self.width, None
            halign: 'left'
            valign: 'top'

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

class ResearchAgentApp(App):
    def build(self):
        print("DEBUG: Entered ResearchAgentApp.build()")
        print("DEBUG: KV string length:", len(KV))
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        Builder.load_string(KV)
        return MainLayout()

    def on_submit(self):
        # TODO: Integrate with agent runner and update markdown_output/status_panel
        self.root.ids.status_panel.text = "Status: Running..."
        # Placeholder for agent execution
        self.root.ids.markdown_output.text = "Running agent... (output will appear here)"

    def on_clear(self):
        self.root.ids.topic_input.text = ""
        self.root.ids.markdown_output.text = ""
        self.root.ids.status_panel.text = "Status: Idle"

    def on_save(self):
        # TODO: Implement file save dialog and save markdown_output.text
        self.root.ids.status_panel.text = "Status: Save feature not yet implemented"

if __name__ == "__main__":
    ResearchAgentApp().run()