## Project Overview

The **AI Research Assistant** is an automated research agent built with [LangChain](https://python.langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph). It takes a research topic, generates search queries, gathers and scrapes web content, summarizes findings, and compiles a structured report.

**Workflow Diagram:**
```mermaid
flowchart TD
    A[Input Topic] --> B[Query Generator]
    B --> C[Web Searcher]
    C --> D[Content Scraper]
    D --> E[Content Summarizer]
    E --> F[Report Compiler]
    F --> G[Output: research_report.md]
```

**Key Features:**
- **Automated Research Pipeline:** Topic → Queries → Web Search → Scraping → Summarization → Report.
- **Stateful Graph Architecture:** Each step is a node in a LangGraph workflow, passing state via a `ResearchState` object.
- **Persistence:** Supports checkpointing with SQLite for workflow recovery.
- **Comprehensive Testing:** Each node and workflow component has dedicated unit tests.

**Code Structure:**
- [`research_graph.py`](research_graph.py:1): Core logic, state definition, node functions, and graph assembly.
- [`workflow_builder.py`](workflow_builder.py:1): Workflow construction and configuration.
- [`agent_runner.py`](agent_runner.py:1): High-level runner for executing the agent and saving reports.
- [`test/`](test/): Unit tests for all components.
- [`requirements.txt`](requirements.txt:1): Dependency list.
- [`.env`](.env): API keys and environment variables.

**APIs & Libraries Used:**
- **LangChain**: LLM orchestration and prompt management.
- **LangGraph**: Graph-based workflow execution.
- **Google Gemini**: LLM for query generation and summarization.
- **Tavily**: Web search API.
- **BeautifulSoup**: HTML parsing and scraping.
- **Requests**: HTTP requests for web scraping.
- **Pytest**: Unit testing framework.

For a step-by-step build guide, see [`Guide.md`](Guide.md:1).
# AI Research Assistant

## Getting Started

Follow these steps to set up and run the AI Research Assistant locally:

### Prerequisites
1. **Python**: Ensure Python 3.8 or newer is installed.
2. **IDE**: Visual Studio Code is recommended.
3. **Internet Access**: Required for research tools and API access.

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv research_agent_env
   ```

3. **Activate the Virtual Environment**:
    - **Windows**:
        ```bash
        research_agent_env\Scripts\activate
        ```
    - **macOS/Linux**:
        ```bash
        source research_agent_env/bin/activate
        ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up API Keys**:
   - Open the `.env` file and add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     LANGCHAIN_TRACING_KEY=your_langchain_tracing_key_here
     ```

### Running the Application
1. **Run the Script**:
   ```bash
   python research_graph.py
   ```

2. **Provide a Research Topic**:
   - The application will prompt you to enter a topic for research.

3. **View the Output**:
   - The final research report will be saved as `research_report.md`.

### Running the AI Agent

You can run the AI Research Assistant programmatically with a provided topic string using [`agent_runner.py`](agent_runner.py:1). This allows you to automate research tasks without manual input.

**Example usage:**
```python
from agent_runner import run_agent

# Replace with your desired research topic
topic = "Recent advances in quantum computing"
final_state = run_agent(topic)

# The final report will be saved as 'research_report.md'
print("Research complete. Report saved.")
```

- The `run_agent` function handles the full workflow: query generation, web search, scraping, summarization, and report compilation.
- Ensure your `.env` file is configured with valid API keys before running the agent.
### Running Unit Tests
To ensure the integrity and correctness of the codebase, run the unit tests using `pytest`.

- **To run all tests:**
  ```bash
  pytest
  ```

- **To run a specific test file:**
  ```bash
  pytest test/test_file_name.py
  ```
  (Replace `test_file_name.py` with the actual name of the test file)

### Notes
- Ensure all API keys are valid and have the necessary permissions.
- For debugging and tracing, consider setting up LangSmith.