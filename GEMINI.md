# Gemini Code Assistant Guidelines

This document outlines the best practices and coding standards for the AI Research Assistant project. Adhering to these guidelines ensures code quality, consistency, and maintainability.

## 0. Prerequisite: Setting up Local Environment
Before starting any development, running any code or tests -- be sure to do the following local setup: 
1. **Create a Virtual Environment**:
   ```bash
   python -m venv research_agent_env
   ```

2. **Activate the Virtual Environment**:
    - **Windows**:
        ```bash
        research_agent_env\Scripts\activate
        ```
    - **macOS/Linux**:
        ```bash
        source research_agent_env/bin/activate
        ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Read over `GEMINI.local.md`**
    - Read the `GEMINI.local.md` file in this repo and adhere to the guidelines outlined exactly as you would the contents of this file

## 1. Python Coding Standards

- **Leverage Modern Python:** Utilize features from Python 3.8+ where appropriate.
- **Dependency Best Practices:** Use `context7` to research the latest and most secure versions of dependencies. Ensure `requirements.txt` is always up-to-date.
- **Type Hinting:** All new functions and methods must include type hints for arguments and return values.

## 2. Consistent Coding Pattern

- **State-Driven Architecture:** The project uses a stateful graph architecture with `LangGraph`. All data flows through the `ResearchState` object.
- **Node-Based Logic:** Each step in the research process is a self-contained "node" function.
- **Immutability:** Nodes should not modify the input state directly. Instead, they return a dictionary of the state updates.

## 3. Unit Testing

- **Mandatory Unit Tests:** All new code, especially new nodes in the research graph, must be accompanied by comprehensive unit tests.
- **Test Coverage:** Tests should validate:
    - **Happy Path:** The expected output for valid inputs.
    - **Edge Cases:** Behavior with empty, invalid, or unusual inputs.
    - **Error Handling:** Proper exception handling and error messages.
- **Test Execution:** All tests must pass before merging new code. Failing tests should be addressed by first evaluating the functional code for bugs, and if none are found, correcting the test.

## 4. Code Quality and Changes

- **Meaningful Changes:** Only make necessary and meaningful changes to the codebase.
- **Optimal and Clean Code:** Write code that is efficient, readable, and well-documented where necessary.
- **Avoid Unnecessary Refactoring:** Do not refactor existing logic unless it is required to fix a bug, improve performance, or is part of a planned architectural change.

## 5. Project Structure

- **`research_graph.py`:** Contains the core logic for the research agent, including the state definition, node functions, and graph assembly.
- **`test_*.py`:** Unit tests for the corresponding components in `research_graph.py`.
- **`.env`:** Stores API keys and other environment variables.
- **`requirements.txt`:** Lists all Python dependencies.
- **`README.md`:** Provides an overview of the project and setup instructions.
- **`ImplementationPlan.md`:** Outlines the development plan and tasks.
- **`Guide.md`:** A step-by-step guide to building the research agent.

# 6. Main Development Process

This document outlines the standard operating procedure for the main development process when engaging with codebases. Following these steps ensures a systematic and collaborative approach to software development, promoting clarity, quality, and efficient progress.

## 6.1 Task Identification & Planning

### Current State Assessment
Before initiating any development work, thoroughly review the `ImplementationPlan.md` document. Concurrently, assess the current state of the entire codebase. This dual review is critical to determine the precise point within the plan where development should resume and to verify that the `ImplementationPlan.md` accurately reflects the project's current status and needs.

### Task Comprehension & Proposed Outline
Once the next task in the `ImplementationPlan.md` has been identified, dedicate sufficient time to fully understand its scope, objectives, and anticipated impact. Following this deep understanding, you are required to formulate and share a detailed outline of your proposed code changes. This outline should clearly articulate:
* **What** specific code modifications, additions, or deletions are planned.
* **How** these changes will be implemented, including the high-level approach, any new dependencies, or architectural considerations.

## 6.2 Approval & Execution

### Plan Approval
Your submitted outline of proposed code changes will be reviewed. Based on this review, you will receive one of the following directives:
* **Approval:** If the plan is approved, you will be explicitly instructed to commence the development work as outlined.
* **Feedback & Revision:** If feedback is provided, you are required to update your plan accordingly, addressing all points raised, and resubmit it for re-approval before proceeding with development.

### Development & Compliance
Upon receiving approval, proceed with the development work. During this phase, it is paramount to ensure that all executed work adheres rigorously to the established standards and guidelines. This includes, but is not limited to, the standards outlined in:
* This current document.
* The `GEMINI.local.md` file (for local environment specific guidelines).
* The overarching `ImplementationPlan.md` document.

## 6.3 Completion & Reporting

### Implementation Plan Update
Once the approved development work has been completed and thoroughly verified against all specified standards, you must update the `ImplementationPlan.md` document. This involves checking off all tasks that have been successfully finished.

### Work Completion Report
After updating the `ImplementationPlan.md`, prepare and share a brief, concise report summarizing the work you have just completed. This report should also include your overall assessment of the codebase's health and integrity, taking into account all the newly integrated changes.

### Subsequent Task Commencement
**Important:** Do not proceed to the next tasks outlined in the `ImplementationPlan.md` document without explicit permission. Always request and await approval before moving on to the subsequent development phases.