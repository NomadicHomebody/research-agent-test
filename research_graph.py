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
llm = GoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0)

def call_llm(messages):
    # GoogleGenerativeAI uses .invoke (not .invoke_llm)
    return llm.invoke(messages)

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
                results = search_tool.invoke(query)
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
    """
    Scrapes the content from the URLs of the retrieved documents.
    Returns a dict with 'scraped_data' and updated 'messages'.
    Handles HTTP errors and cases where no documents are found.
    """
    docs = state.get("retrieved_docs", [])
    messages = state.get("messages", []).copy()
    scraped_data = []
    error_message = ""

    if not docs:
        error_message = "No documents to scrape."
        messages.append({"role": "system", "content": error_message})
        return {
            "scraped_data": [],
            "messages": messages,
            "error_message": error_message
        }

    for doc in docs:
        url = doc.get("url")
        if not url:
            continue
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Attempt to find the main content, fall back to body
            main_content = soup.find("article") or soup.find("main") or soup.body
            if main_content:
                # Remove script and style elements
                for script_or_style in main_content(["script", "style"]):
                    script_or_style.decompose()
                text = main_content.get_text(separator="\n", strip=True)
            else:
                text = ""

            scraped_data.append({"url": url, "content": text[:5000]}) # Limit content size
            messages.append({"role": "system", "content": f"Successfully scraped {url}"})

        except requests.RequestException as e:
            messages.append({"role": "system", "content": f"Failed to scrape {url}: {e}"})
        except Exception as e:
            messages.append({"role": "system", "content": f"An unexpected error occurred while scraping {url}: {e}"})

    return {
        "scraped_data": scraped_data,
        "messages": messages,
        "error_message": ""
    }

def summarize_content_node(state: ResearchState) -> Dict[str, Any]:
    """
    Summarizes the scraped content for each document based on the research topic.
    Returns a dict with 'summaries' and updated 'messages'.
    Handles LLM errors and cases where no content is available for summarization.
    """
    topic = state.get("topic", "")
    scraped_data = state.get("scraped_data", [])
    messages = state.get("messages", []).copy()
    summaries = []
    error_message = ""
    has_errors = False

    if not scraped_data:
        error_message = "No scraped content available to summarize."
        messages.append({"role": "system", "content": error_message})
        return {
            "summaries": [],
            "messages": messages,
            "error_message": error_message
        }

    for item in scraped_data:
        url = item.get("url")
        content = item.get("content")

        if not content or not content.strip():
            messages.append({"role": "system", "content": f"Skipping summarization for {url} due to empty content."})
            continue

        try:
            prompt = ChatPromptTemplate.from_template(
                "Given the research topic: '{topic}' and the following content from a webpage, "
                "please provide a concise summary that is relevant to the topic. "
                "Focus on extracting key facts, figures, and main arguments.\n\n"
                "Content:\n{content}"
            ).format(topic=topic, content=content)

            llm_response = call_llm([HumanMessage(content=prompt)])
            summary = llm_response.content if hasattr(llm_response, "content") else str(llm_response)
            
            if summary.strip():
                summaries.append(summary)
                messages.append({"role": "system", "content": f"Successfully summarized content from {url}."})
            else:
                messages.append({"role": "system", "content": f"LLM returned an empty summary for {url}."})
                has_errors = True

        except Exception as e:
            messages.append({"role": "system", "content": f"Error summarizing content from {url}: {str(e)}"})
            has_errors = True
            continue

    if not summaries and has_errors:
        error_message = "Could not generate any summaries due to errors."
        messages.append({"role": "system", "content": error_message})
    elif not summaries:
        error_message = "Could not generate any summaries from the provided content."
        messages.append({"role": "system", "content": error_message})

    return {
        "summaries": summaries,
        "messages": messages,
        "error_message": error_message if not summaries else ""
    }

def compile_report_node(state: ResearchState) -> Dict[str, Any]:
    """
    Compiles the summaries into a final, structured research report.
    Returns a dict with 'final_report' and updated 'messages'.
    Handles cases where no summaries are available.
    """
    topic = state.get("topic", "")
    summaries = state.get("summaries", [])
    messages = state.get("messages", []).copy()
    error_message = ""

    if not summaries:
        error_message = "No summaries available to compile a report."
        messages.append({"role": "system", "content": error_message})
        return {
            "final_report": "",
            "messages": messages,
            "error_message": error_message
        }

    try:
        # Join summaries into a single string for the prompt
        summaries_str = "\n\n---\n\n".join(summaries)

        prompt = ChatPromptTemplate.from_template(
            "Given the research topic: '{topic}' and the following summaries from various sources, "
            "synthesize them into a comprehensive, well-structured, and formal research report. "
            "The report should have a clear introduction, body, and conclusion. "
            "Use markdown for formatting (e.g., headers, lists, bold text).\n\n"
            "Summaries:\n{summaries}"
        ).format(topic=topic, summaries=summaries_str)

        llm_response = call_llm([HumanMessage(content=prompt)])
        final_report = llm_response.content if hasattr(llm_response, "content") else str(llm_response)

        messages.append({"role": "system", "content": "Successfully compiled the final report."})

        return {
            "final_report": final_report,
            "messages": messages,
            "error_message": ""
        }
    except Exception as e:
        error_message = f"Error compiling the final report: {str(e)}"
        messages.append({"role": "system", "content": error_message})
        return {
            "final_report": "",
            "messages": messages,
            "error_message": error_message
        }
