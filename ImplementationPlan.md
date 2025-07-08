# 9. UI Modernization & Layout Update Implementation Plan

## Objective
Implement the following UI changes in the main codebase and ensure all impacted and new tests are updated and passing:
1. All UI text is black or dark blue.
2. Input box, buttons, and status box are on the left half, stacked vertically.
3. Status box has a light grey background and dark blue text.
4. Markdown window is on the right half, widened, and renders "pretty" markdown.
5. All tests validate new UI logic and pass.

---

## Implementation Steps

### 1. Update Main Layout and Styling ([`gui/main.py`])
- Refactor the KV string:
  - Ensure left `BoxLayout` contains, in order: `TextInput`, buttons (`Submit`, `Clear`, `Save`), and the `StatusPanel` widget (replace the label).
  - Set `color` property for all text widgets to black (`0,0,0,1`) or dark blue (`0,0.12,0.3,1`).
  - Adjust `size_hint_x` and `size_hint_y` to ensure left and right halves are equal and content fills available space.
- Update button and input styling for consistency.

### 2. Status Panel Styling ([`gui/widgets/status_panel.py`])
- Add a `Label` child to `StatusPanel` that binds to `status_text`.
- Use Kivy canvas to set a light grey background (`#f0f0f0`).
- Set label text color to dark blue.
- Ensure the widget stretches horizontally and vertically as needed.

### 3. Markdown Viewer Rendering ([`gui/widgets/markdown_viewer.py`])
- Replace the `Label` with a widget that supports HTML (e.g., `kivy.uix.webview` or a rich text widget).
- On `markdown_text` update, convert markdown to HTML using the `markdown` package and display formatted output.
- Ensure indentation, lists, code blocks, and other markdown features render correctly.

### 4. Test Updates and Creation ([`gui/tests/`])
- Update or create tests in:
  - [`test_main.py`]: Validate layout, widget placement, and color properties.
  - [`test_widgets.py`]: Test `StatusPanel` background/text color and markdown rendering.
- Add tests to:
  - Confirm all UI elements are present and styled as specified.
  - Validate markdown rendering for various markdown features.
  - Check status panel color and text updates.
- Run all tests and ensure they pass.
  - If a test fails, first check for bugs in the main code and fix as needed.
  - If no bug is found, fix the test and re-run.

### 5. Documentation
- Add/expand docstrings in all modified classes and methods.
- Update comments to clarify layout and styling logic.

---

## Acceptance Criteria
- All UI changes are visible and match requirements.
- All tests pass and cover new/updated logic.
- No regressions in existing functionality.
- Plan is documented in this section.

---

## Implementation Steps

### 1. Update Main Layout and Styling ([`gui/main.py`])
- Refactor the KV string:
  - Ensure left `BoxLayout` contains, in order: `TextInput`, buttons (`Submit`, `Clear`, `Save`), and the `StatusPanel` widget (replace the label).
  - Set `color` property for all text widgets to black (`0,0,0,1`) or dark blue (`0,0.12,0.3,1`).
  - Adjust `size_hint_x` and `size_hint_y` to ensure left and right halves are equal and content fills available space.
- Update button and input styling for consistency.

### 2. Status Panel Styling ([`gui/widgets/status_panel.py`])
- Add a `Label` child to `StatusPanel` that binds to `status_text`.
- Use Kivy canvas to set a light grey background (`#f0f0f0`).
- Set label text color to dark blue.
- Ensure the widget stretches horizontally and vertically as needed.

### 3. Markdown Viewer Rendering ([`gui/widgets/markdown_viewer.py`])
- Replace the `Label` with a widget that supports HTML (e.g., `kivy.uix.webview` or a rich text widget).
- On `markdown_text` update, convert markdown to HTML using the `markdown` package and display formatted output.
- Ensure indentation, lists, code blocks, and other markdown features render correctly.

### 4. Test Updates and Creation ([`gui/tests/`])
- Update or create tests in:
  - [`test_main.py`]: Validate layout, widget placement, and color properties.
  - [`test_widgets.py`]: Test `StatusPanel` background/text color and markdown rendering.
- Add tests to:
  - Confirm all UI elements are present and styled as specified.
  - Validate markdown rendering for various markdown features.
  - Check status panel color and text updates.
- Run all tests and ensure they pass.
  - If a test fails, first check for bugs in the main code and fix as needed.
  - If no bug is found, fix the test and re-run.

### 5. Documentation
- Add/expand docstrings in all modified classes and methods.
- Update comments to clarify layout and styling logic.

---

## Acceptance Criteria
- All UI changes are visible and match requirements.
- All tests pass and cover new/updated logic.
- No regressions in existing functionality.
- Plan is documented in this section.

