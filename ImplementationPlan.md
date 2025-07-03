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

- [ ] Implement `compile_report_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] Prompt LLM to synthesize summaries into a structured report.
  - [ ] Return `{"final_report": report, "messages": ...}`.
  - [ ] **Add unit tests for Report Compiler Node**
    - [ ] Test happy path: valid summaries return report.
    - [ ] Test edge cases: empty summaries, malformed summaries.
    - [ ] Test exception handling: LLM errors, formatting errors.
      - If test(s) fail: evaluate the functional validity of the main logic first to see if there is a bug:
        - If there is a bug then edit the main logic to fix the bug
        - If no bug is evident then fix the test

---

## 4. Build the LangGraph Workflow

- [ ] Instantiate graph:  
  `workflow = StateGraph(ResearchState)`
- [ ] Add nodes:  
  `workflow.add_node("query_generator", generate_queries_node)`  
  (repeat for each node)
- [ ] Add edges:  
  `workflow.add_edge("query_generator", "web_searcher")`  
  (repeat for each transition)
- [ ] Set entry point:  
  `workflow.set_entry_point("query_generator")`
- [ ] Set terminal node:  
  `workflow.add_edge("report_compiler", END)`

---

## 5. Set Up Persistence (Optional)

- [ ] Add persistence:  
  `from langgraph.checkpoint.sqlite import SqliteSaver`  
  `memory = SqliteSaver.from_conn_string(":memory:")`
- [ ] Compile with checkpointing:  
  `app = workflow.compile(checkpointer=memory)`

---

## 6. Run the Graph, Display, and Save Results

- [ ] Prepare input:  
  `inputs = {"topic": "Your research topic", "messages": [HumanMessage(content="Start research on: ...")]}`
- [ ] Run graph:  
  `for output_chunk in app.stream(inputs, config=config, stream_mode="values"): ...`
- [ ] Get final state:  
  `final_state = app.get_state(config)`
- [ ] Save report:  
  `with open("research_report.md", "w", encoding="utf-8") as f: f.write(final_state.values["final_report"])`

---

## Mermaid Diagram

```mermaid
flowchart TD
    A[Input Topic] --> B[Query Generator]
    B --> C[Web Searcher]
    C --> D[Content Scraper]
    D --> E[Content Summarizer]
    E --> F[Report Compiler]
    F --> G[Output: research_report.md]