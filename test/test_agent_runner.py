import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock, mock_open
from agent_runner import run_agent

@patch('agent_runner.build_workflow')
@patch('builtins.open', new_callable=mock_open)
def test_run_agent(mock_open_func, mock_build_workflow):
    """
    Tests the agent runner to ensure it executes the workflow and saves the report.
    """
    # Mock the compiled workflow
    mock_app = MagicMock()
    mock_build_workflow.return_value = mock_app

    # Mock the state returned by the workflow
    mock_final_state = MagicMock()
    mock_final_state.values = {"final_report": "This is the final research report."}
    mock_app.get_state.return_value = mock_final_state

    # Mock the stream to simulate the workflow execution
    mock_app.stream.return_value = [
        {"key": "value1"},
        {"key": "value2"}
    ]

    # Run the agent
    run_agent("Test Topic")

    # Assert that the workflow was built and called
    mock_build_workflow.assert_called_once()
    mock_app.stream.assert_called_once()
    mock_app.get_state.assert_called_once()

    # Assert that the report file was written correctly
    mock_open_func.assert_called_once_with("research_report.md", "w", encoding="utf-8")
    mock_open_func().write.assert_called_once_with("This is the final research report.")
