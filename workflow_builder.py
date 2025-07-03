from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from research_graph import (
    ResearchState,
    generate_queries_node,
    web_search_node,
    scrape_content_node,
    summarize_content_node,
    compile_report_node
)

def build_workflow():
    """
    Builds the LangGraph workflow for the research agent.

    Returns:
        A compiled LangGraph workflow with checkpointing.
    """
    memory = MemorySaver()
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("query_generator", generate_queries_node)
    workflow.add_node("web_searcher", web_search_node)
    workflow.add_node("content_scraper", scrape_content_node)
    workflow.add_node("content_summarizer", summarize_content_node)
    workflow.add_node("report_compiler", compile_report_node)

    # Add edges
    workflow.set_entry_point("query_generator")
    workflow.add_edge("query_generator", "web_searcher")
    workflow.add_edge("web_searcher", "content_scraper")
    workflow.add_edge("content_scraper", "content_summarizer")
    workflow.add_edge("content_summarizer", "report_compiler")
    workflow.add_edge("report_compiler", END)

    return workflow.compile(checkpointer=memory)
