import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from research_graph import compile_report_node, ResearchState

# Mock the llm object directly
@pytest.fixture
def mock_llm():
    with patch('research_graph.llm') as mock_llm_instance:
        # The invoke method should return a MagicMock that has a 'content' attribute
        mock_invoke_result = MagicMock()
        mock_invoke_result.content = "This is the final report."
        mock_llm_instance.invoke.return_value = mock_invoke_result
        yield mock_llm_instance

def test_compile_report_node_happy_path(mock_llm):
    """
    Tests the happy path where valid summaries are compiled into a report.
    """
    state = ResearchState(
        topic="Test Topic",
        summaries=["Summary 1", "Summary 2"],
        messages=[]
    )
    result = compile_report_node(state)
    
    assert "final_report" in result
    assert isinstance(result["final_report"], str)
    assert result["final_report"] == "This is the final report."
    assert "Error" not in result.get("error_message", "")
    # Ensure the LLM was called
    mock_llm.invoke.assert_called_once()

def test_compile_report_node_empty_summaries(mock_llm):
    """
    Tests the edge case where the list of summaries is empty.
    """
    state = ResearchState(
        topic="Test Topic",
        summaries=[],
        messages=[]
    )
    result = compile_report_node(state)
    
    assert "final_report" in result
    assert result["final_report"] == ""
    assert "error_message" in result
    assert "No summaries available to compile a report" in result["error_message"]
    # Ensure the LLM was not called
    mock_llm.invoke_llm.assert_not_called()
