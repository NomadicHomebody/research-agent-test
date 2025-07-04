# Implementation Plan: Research Agent with LangChain & LangGraph

## 1. Project Setup, Imports, and Environment Initialization

- [x] **Create virtual environment:**  
  `python -m venv research_agent_env`
- [x] **Activate environment:**  
  Windows: `research_agent_env\Scripts\activate`
- [x] **Install dependencies:**  
  `pip install langchain langgraph langchain_google_genai python-dotenv beautifulsoup4 tavily-python`
- [x] **Create `.env` file:**  
  Add API keys for Google Gemini, Tavily, and optionally LangSmith.
- [x] **Import modules in `research_graph.py`:**
  - `os`, `dotenv`, `typing`, `operator`
  - `from langchain_google_genai import ChatGoogleGemini`
  - `from langchain_community.tools.tavily_search import TavilySearchResults`
  - `from langchain_core.prompts import ChatPromptTemplate`
  - `from langgraph.graph import StateGraph`
  - `from langchain_core.messages import HumanMessage`
  - `from bs4 import BeautifulSoup`
  - `import requests`
- [x] **Load environment variables:**  
  `from dotenv import load_dotenv; load_dotenv()`
- [x] **Initialize LLM:**  
  `llm = ChatGoogleGemini(model="gemini-1", temperature=0)`

---

## 2. Define the Research Agent State Graph Structure

- [x] **Define `ResearchState` using `TypedDict`:**
  ```python
  class ResearchState(TypedDict):
      topic: str
      search_queries: list[str]
      retrieved_docs: list[dict]
      scraped_data: list[dict]
      summaries: list[str]
      final_report: str
      error_message: str
      messages: list
  ```
- [x] **Plan node sequence:**  
  Query Generator → Web Searcher → Content Scraper → Content Summarizer → Report Compiler

---

## 3. Implement Node Functions

### a. Query Generator Node

- [x] Implement `generate_queries_node(state: ResearchState) -> Dict[str, Any]`
  - [x] Use `ChatPromptTemplate` to prompt LLM for 3-5 search queries.
  - [x] Parse LLM output into a list of queries.
  - [x] Return `{"search_queries": queries, "messages": ...}`.
  - [x] **Add unit tests for Query Generator Node**
    - [x] Create new test file and setup all required inputs and env var loading for proper testing
    - [x] Test happy path: valid topic returns list of queries.
    - [x] Test edge cases: empty topic, non-string topic.
    - [x] Test exception handling: LLM errors, parsing errors.
    - [x] Run all tests and validate that they all pass
      - If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - If there is a bug then edit the main logic to fix the bug
        - If no bug is evident then fix the test

###`    b. Web Searcher Node/q
- [x] Implement `web_search_node(state: ResearchState) -> Dict[str, Any]`
  - [x] Use `TavilySearchResults(max_results=3)` for each query.
  - [x] Collect and deduplicate URLs/snippets.
  - [x] Return `{"retrieved_docs": docs, "messages": ...}`.
  - [x] **Add unit tests for Web Searcher Node**
    - [x] Test happy path: valid queries return docs.
    - [x] Test edge cases: empty queries, duplicate queries.
    - [x] Test exception handling: API errors, network failures.
    - [x] Run all tests and validate that they all pass
      - If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - If there is a bug then edit the main logic to fix the bug
        - If no bug is evident then fix the test

### c. Content Scraper Node

- [x] Implement `scrape_content_node(state: ResearchState) -> Dict[str, Any]`
  - [x] For each URL, fetch HTML with `requests.get(url)`.
  - [x] Extract main text using `BeautifulSoup`.
  - [x] Return `{"scraped_data": scraped_results, "messages": ...}`.
  - [x] **Add unit tests for Content Scraper Node**
    - [x] Test happy path: valid URLs return scraped content.
    - [x] Test edge cases: invalid URLs, empty content.
    - [x] Test exception handling: HTTP errors, parsing errors.
    - [x] Run all tests and validate that they all pass
      - If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - If there is a bug then edit the main logic to fix the bug
        - If no bug is evident then fix the test

### d. Content Summarizer Node

- [x] Implement `summarize_content_node(state: ResearchState) -> Dict[str, Any]`
  - [x] For each page, prompt LLM to summarize content relevant to topic.
  - [x] Return `{"summaries": summaries, "messages": ...}`.
  - [x] **Add unit tests for Content Summarizer Node**
    - [x] Test happy path: valid content returns summaries.
    - [x] Test edge cases: empty content, irrelevant content.
    - [x] Test exception handling: LLM errors, empty summaries.
      - [x] If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - [x] If there is a bug then edit the main logic to fix the bug
        - [x] If no bug is evident then fix the test

### e. Report Compiler Node

- [x] Implement `compile_report_node(state: ResearchState) -> Dict[str, Any]`
  - [x] Prompt LLM to synthesize summaries into a structured report.
  - [x] Return `{"final_report": report, "messages": ...}`.
  - [x] **Add unit tests for Report Compiler Node**
    - [x] Test happy path: valid summaries return report.
    - [x] Test edge cases: empty summaries, malformed summaries.
    - [x] Test exception handling: LLM errors, formatting errors.
      - [x] If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - [x] If there is a bug then edit the main logic to fix the bug
        - [x] If no bug is evident then fix the test

---

## 4. Build the LangGraph Workflow

- [x] Create a new file `workflow_builder.py` for storing new code
- [x] Create new method `build_workflow` that returns a newly instanciated workflow
- [x] Instantiate graph:  
  `workflow = StateGraph(ResearchState)`
- [x] Add nodes:  
  `workflow.add_node("query_generator", generate_queries_node)`  
  (repeat for each node)
- [x] Add edges:  
  `workflow.add_edge("query_generator", "web_searcher")`  
  (repeat for each transition)
- [x] Set entry point:  
  `workflow.set_entry_point("query_generator")`
- [x] Set terminal node:  
  `workflow.add_edge("report_compiler", END)`
- [x] **Add unit tests for workflow_builder**
  - [x] Test happy path: valid summaries return report.
  - [x] Test edge cases: empty summaries, malformed summaries.
  - [x] Test exception handling: LLM errors, formatting errors.
    - [x] If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
      - [x] If there is a bug then edit the main logic to fix the bug
      - [x] If no bug is evident then fix the test
---

## 5. Set Up Persistence (Optional)

- [x] Add persistence:  
  `from langgraph.checkpoint.sqlite import SqliteSaver`  
  `memory = SqliteSaver.from_conn_string(":memory:")`
- [x] Compile with checkpointing:  
  `app = workflow.compile(checkpointer=memory)`
- [x] **Add unit tests for new persistence logic**
  - [x] Test happy path
  - [x] Test edge cases
  - [x] Test exception handling
    - [x] If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
      - [x] If there is a bug then edit the main logic to fix the bug
      - [x] If no bug is evident then fix the test
---

## 6. Set Up Agent Runner 

- [x] Create new file `agent_runner` that streamlines the execution for running the AI agent workflow such that all it takes is an input string of the desired research topic into a method to get the AI agent to fully execute, retrieve the final state, and save the final report to a markdown file like the high level flow listed below:
- [x] **Add unit tests for workflow_builder**
  - [x] Test happy path: valid summaries return report.
  - [x] Test edge cases: empty summaries, malformed summaries.
  - [x] Test exception handling: LLM errors, formatting errors.
    - [x] If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
      - [x] If there is a bug then edit the main logic to fix the bug
      - [x] If no bug is evident then fix the test
---

## 7. CLI Runner with Spinner and Status Updates

- [x] Refactor workflow to support explicit node-by-node status yielding via `stepwise_agent` in [`workflow_builder.py`](workflow_builder.py:12)
- [x] Replace `agent_runner.py` with CLI runner that:
    - Accepts a topic string from the command line
    - Uses `yaspin` spinner and updates status as each node completes
    - Writes the markdown report to `research_report.md`
    - Prints a final message with the report location
- [x] Add/modify unit tests in `test/test_agent_runner.py` to cover spinner/status logic and file output
- [x] Add `yaspin` to `requirements.txt`
- [ ] (Optional) Run Bandit security scan

## 8. Add UI Wrapper for Agent AI

- [ ] Research best implementation stratgies for leveraging the Kivy library for implementing UIs with the following features:
  - Clean and modern looking UI
  - Takes in text input
  - Has buttons for submitting text, emptying the text input box, saving the resulting output file to a desired location
  - Displays status updates
  - Displays the resulting markdown file in its "pretty" state in a window beside the text input
  - Re-sizable window with UI that automatically adjusts to best fit the window size
  - Dynamic background that changes the color based on the location of the mouse
- [ ] Develop Implementation plan based on research results and update this step with a clear plan for implementing a UI that meets the following requirements:
  - Clean, cohesive and modern looking UI with sleek labeling for inputs, buttons, windows with the following layout:
    - Input box for research topic in the left half of the window that takes up around 3/5ths of the vertical space of the window (when factoring in proper padding for everything)
    - a SVG logo in the bottom left corner of the GUI of a magnifying glass with the letters `AI` in it and the words `AI Research Agent` centered under it
    - Should take up about 1/5th of the vertical space of the window (when factoring in proper padding for everything)
    - Has buttons for submitting text, emptying the text input box, saving the resulting output file to a desired location that are all represented by nice SVG icons
      - Should be in the left half of the screen above the SVG logo and below the input text box for the topic
      - Should take up about 1/5th of the vertical space of the window (when factoring in proper padding for everything)
    - Bottom right corner has a status window that displays icons and text informing the user of the status of the AI reserch agent while running/inactive
      - Sould be on the right half of the screen and take up about 1/6th of the vertical space of the window (when factoring in proper padding for everything)
    - Displays the resulting markdown file in its "pretty" state in a window beside the text input
      - Sould be on the right half of the screen and take up about 5/6ths of the vertical space of the window (when factoring in proper padding for everything)
  - Re-sizable window with UI that automatically adjusts to best fit the window size
  - Dynamic background that changes the color based on the location of the mouse
  - All elements in GUI should be spaced evenly with logical centering in mind
  - Color theme should be a mix or dark and light colors with clean gradients (black, grey, blue, white, green)
  - Font, texts, outputs and icons should all be clear, easy to read and placed in sensible locations within the window space
  - Unit tests are implemented for all the new code required for the GUI
  - GUI code can be written in a single or multiple files (whatever makes logical sense for maintaining organized code structure)

```mermaid
flowchart TD
    A[Input Topic] --> B[Query Generator]
    B --> C[Web Searcher]
    C --> D[Content Scraper]
    D --> E[Content Summarizer]
    E --> F[Report Compiler]
    F --> G[Output: research_report.md]