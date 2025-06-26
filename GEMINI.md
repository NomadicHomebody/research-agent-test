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
