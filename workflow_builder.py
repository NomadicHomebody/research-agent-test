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

def stepwise_agent(topic: str):
    """
    Generator that yields (node_name, status_message, state) after each node in the workflow.
    Args:
        topic: The research topic.
    Yields:
        Tuple of (node_name, status_message, current_state)
    """
    from langchain_core.messages import HumanMessage
    import uuid

    app = build_workflow()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    inputs = {"topic": topic, "messages": [HumanMessage(content=f"Start research on: {topic}")]}
    node_order = [
        ("query_generator", "Generating search queries..."),
        ("web_searcher", "Performing web search..."),
        ("content_scraper", "Scraping web content..."),
        ("content_summarizer", "Summarizing content..."),
        ("report_compiler", "Compiling final report...")
    ]
    node_idx = 0
    for output_chunk in app.stream(inputs, config=config, stream_mode="values"):
        if node_idx < len(node_order):
            node_name, status_message = node_order[node_idx]
        else:
            node_name, status_message = ("unknown", "Processing...")
        # Debug: print state at each node
        print(f"[DEBUG] Node: {node_name}, State keys: {list(output_chunk.keys())}")
        if "final_report" in output_chunk:
            print(f"[DEBUG] Node: {node_name}, final_report: {output_chunk['final_report'][:100]}")
        if "search_queries" in output_chunk:
            print(f"[DEBUG] Node: {node_name}, search_queries: {output_chunk['search_queries']}")
        if "retrieved_docs" in output_chunk:
            print(f"[DEBUG] Node: {node_name}, retrieved_docs: {output_chunk['retrieved_docs']}")
        if "error_message" in output_chunk and output_chunk["error_message"]:
            print(f"[DEBUG] Node: {node_name}, error_message: {output_chunk['error_message']}")
        yield node_name, status_message, output_chunk
        node_idx += 1
    # Final state
    final_state = app.get_state(config)
    print(f"[DEBUG] Final state keys: {list(final_state.values.keys())}")
    if "final_report" in final_state.values:
        print(f"[DEBUG] Final final_report: {final_state.values['final_report'][:100]}")
    yield "done", "Report generated.", final_state.values
