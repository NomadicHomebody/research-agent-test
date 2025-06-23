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

- [ ] Implement `generate_queries_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] Use `ChatPromptTemplate` to prompt LLM for 3-5 search queries.
  - [ ] Parse LLM output into a list of queries.
  - [ ] Return `{"search_queries": queries, "messages": ...}`.

### b. Web Searcher Node

- [ ] Implement `web_search_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] Use `TavilySearchResults(max_results=3)` for each query.
  - [ ] Collect and deduplicate URLs/snippets.
  - [ ] Return `{"retrieved_docs": docs, "messages": ...}`.

### c. Content Scraper Node

- [ ] Implement `scrape_content_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] For each URL, fetch HTML with `requests.get(url)`.
  - [ ] Extract main text using `BeautifulSoup`.
  - [ ] Return `{"scraped_data": scraped_results, "messages": ...}`.

### d. Content Summarizer Node

- [ ] Implement `summarize_content_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] For each page, prompt LLM to summarize content relevant to topic.
  - [ ] Return `{"summaries": summaries, "messages": ...}`.

### e. Report Compiler Node

- [ ] Implement `compile_report_node(state: ResearchState) -> Dict[str, Any]`
  - [ ] Prompt LLM to synthesize summaries into a structured report.
  - [ ] Return `{"final_report": report, "messages": ...}`.

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