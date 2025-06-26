import os
from dotenv import load_dotenv
from typing import TypedDict, List, Dict, Any
from operator import itemgetter

from langchain_google_genai import GoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from bs4 import BeautifulSoup
import requests

# 1. Load environment variables
load_dotenv()

# 2. Initialize LLM
llm = GoogleGenerativeAI(model="gemini-1.0-pro", temperature=0)

def call_llm(messages):
    # GoogleGenerativeAI uses .invoke_llm instead of .invoke
    return llm.invoke_llm(messages)

# 3. Define ResearchState TypedDict
class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    retrieved_docs: List[Dict[str, Any]]
    scraped_data: List[Dict[str, Any]]
    summaries: List[str]
    final_report: str
    error_message: str
    messages: List[Any]

# --- Node function stubs (to be implemented in next steps) ---

def generate_queries_node(state: ResearchState) -> Dict[str, Any]:
    """
    Generates 3-5 effective search queries for the given research topic using the LLM.
    Returns a dict with 'search_queries' and updated 'messages'.
    Handles empty/non-string topics and LLM/parsing errors.
    """
    topic = state.get("topic", "")
    messages = state.get("messages", []).copy()
    queries = []
    error_message = ""

    # Edge case: topic must be a non-empty string
    if not isinstance(topic, str) or not topic.strip():
        error_message = "Invalid topic: must be a non-empty string."
        messages.append({"role": "system", "content": error_message})
        return {
            "search_queries": [],
            "messages": messages,
            "error_message": error_message
        }

    try:
        prompt = ChatPromptTemplate.from_template(
            "Given the research topic: '{topic}', generate 3-5 effective search queries that would help find relevant information online. "
            "Return the queries as a numbered list."
        ).format(topic=topic.strip())

        llm_response = call_llm([HumanMessage(content=prompt)])

        # Parse queries from LLM response (expects numbered list)
        import re
        raw = llm_response.content if hasattr(llm_response, "content") else str(llm_response)
        queries = [q.strip("- ").strip() for q in re.findall(r"(?:\d+\.|\-)\s*(.+)", raw) if q.strip()]
        if not queries:
            # fallback: split by lines if no numbers found
            queries = [line.strip("- ").strip() for line in raw.splitlines() if line.strip()]

        # Only keep 3-5 queries
        queries = queries[:5]

        messages.append({"role": "system", "content": f"Generated queries: {queries}"})

        return {
            "search_queries": queries,
            "messages": messages,
            "error_message": ""
        }
    except Exception as e:
        error_message = f"Error generating queries: {str(e)}"
        messages.append({"role": "system", "content": error_message})
        return {
            "search_queries": [],
            "messages": messages,
            "error_message": error_message
        }

def web_search_node(state: ResearchState) -> Dict[str, Any]:
    """
    Performs web searches for each query, collects and deduplicates results.
    Returns a dict with 'retrieved_docs' and updated 'messages'.
    Handles API errors and empty search results.
    """
    queries = state.get("search_queries", [])
    messages = state.get("messages", []).copy()
    all_docs = []
    error_message = ""

    if not queries:
        error_message = "No search queries provided."
        messages.append({"role": "system", "content": error_message})
        return {
            "retrieved_docs": [],
            "messages": messages,
            "error_message": error_message
        }

    try:
        search_tool = TavilySearchResults(max_results=3)
        for query in queries:
            try:
                results = search_tool.invoke([{"query": query}])
                all_docs.extend(results)
            except Exception as e:
                messages.append({"role": "system", "content": f"Search failed for query '{query}': {e}"})
                # Continue to next query
                continue

        # Deduplicate docs based on 'url'
        unique_docs = {doc['url']: doc for doc in all_docs}.values()
        all_docs = list(unique_docs)

        messages.append({"role": "system", "content": f"Retrieved {len(all_docs)} unique documents."})

        return {
            "retrieved_docs": all_docs,
            "messages": messages,
            "error_message": ""
        }
    except Exception as e:
        error_message = f"An unexpected error occurred during web search: {str(e)}"
        messages.append({"role": "system", "content": error_message})
        return {
            "retrieved_docs": [],
            "messages": messages,
            "error_message": error_message
        }

def scrape_content_node(state: ResearchState) -> Dict[str, Any]:
    # TODO: Implement content scraping logic
    return {}

def summarize_content_node(state: ResearchState) -> Dict[str, Any]:
# --- Example: How to run the workflow (to be completed after workflow assembly) ---

# Example usage:
# if __name__ == "__main__":
#     topic_to_research = "The impact of AI on creative writing"
#     config = {"configurable": {"thread_id": "research-thread-1"}}
#     inputs = {
#         "topic": topic_to_research,
#         "messages": [HumanMessage(content=f"Start research on: {topic_to_research}")]
#     }
#     for output_chunk in app.stream(inputs, config=config, stream_mode="values"):
#         print(output_chunk)
#     final_state = app.get_state(config)
#     print(final_state.values["final_report"])
#     with open("research_report.md", "w", encoding="utf-8") as f:
#         f.write(final_state.values["final_report"])
# --- LangGraph workflow assembly (to be completed after node implementations) ---

# Example (to be expanded in next steps):
# workflow = StateGraph(ResearchState)
# workflow.add_node("query_generator", generate_queries_node)
# workflow.add_node("web_searcher", web_search_node)
# workflow.add_node("content_scraper", scrape_content_node)
# workflow.add_node("content_summarizer", summarize_content_node)
# workflow.add_node("report_compiler", compile_report_node)
# workflow.set_entry_point("query_generator")
# workflow.add_edge("query_generator", "web_searcher")
# workflow.add_edge("web_searcher", "content_scraper")
# workflow.add_edge("content_scraper", "content_summarizer")
# workflow.add_edge("content_summarizer", "report_compiler")
# workflow.add_edge("report_compiler", END)
    # TODO: Implement summarization logic
    return {}

def compile_report_node(state: ResearchState) -> Dict[str, Any]:
    # TODO: Implement report compilation logic
    return {}

# --- End of initial scaffolding ---