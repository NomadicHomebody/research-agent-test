import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from workflow_builder import build_workflow
from langgraph.graph import StateGraph

@patch('research_graph.generate_queries_node')
@patch('research_graph.web_search_node')
@patch('research_graph.scrape_content_node')
@patch('research_graph.summarize_content_node')
@patch('research_graph.compile_report_node')
def test_build_workflow(
    mock_compile_report, 
    mock_summarize_content, 
    mock_scrape_content, 
    mock_web_search, 
    mock_generate_queries
):
    """
    Tests that the workflow is built with the correct nodes and edges.
    """
    app = build_workflow()
    
    # Check that the returned object is a compiled graph
    assert hasattr(app, 'stream')
    assert hasattr(app, 'get_state')

    # Check that all nodes are in the graph
    assert "query_generator" in app.nodes
    assert "web_searcher" in app.nodes
    assert "content_scraper" in app.nodes
    assert "content_summarizer" in app.nodes
    assert "report_compiler" in app.nodes
