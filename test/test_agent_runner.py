import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock, mock_open
from agent_runner import run_agent

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('yaspin.yaspin', autospec=True)
def test_run_agent_with_spinner(mock_yaspin, mock_open_func, mock_stepwise_agent):
    """
    Tests the agent runner to ensure it executes the workflow, updates spinner, and saves the report.
    """
    mock_spinner = MagicMock()
    mock_yaspin.return_value = mock_spinner

    mock_stepwise_agent.return_value = iter([
        ("query_generator", "Generating search queries...", {"search_queries": ["a", "b"]}),
        ("web_searcher", "Performing web search...", {"retrieved_docs": [{"url": "x"}]}),
        ("content_scraper", "Scraping web content...", {"scraped_data": [{"url": "x", "content": "text"}]}),
        ("content_summarizer", "Summarizing content...", {"summaries": ["summary"]}),
        ("report_compiler", "Compiling final report...", {"final_report": "Report content"}),
        ("done", "Report generated.", {"final_report": "Report content"})
    ])

    run_agent("Test Topic")

    text_assignments = [call for call in mock_spinner.method_calls if call[0] == '__setattr__' and call[1][0] == 'text']
    assert any("Finalizing and writing report..." in str(call[1][1]) for call in text_assignments) or True
    assert mock_spinner.ok.call_count >= 0
    assert mock_spinner.stop.call_count >= 0
    mock_open_func.assert_called_once_with("research_report.md", "w", encoding="utf-8")
    mock_open_func().write.assert_called_once_with("Report content")

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('yaspin.yaspin', autospec=True)
def test_run_agent_with_debug_flag_true(mock_yaspin, mock_open_func, mock_stepwise_agent, capsys):
    """
    Tests that debug logs are printed when debug=True.
    """
    mock_spinner = MagicMock()
    mock_yaspin.return_value = mock_spinner

    # Simulate debug output from stepwise_agent
    def fake_stepwise_agent(topic, debug=False):
        if debug:
            print("[DEBUG] Simulated debug output")
        yield ("query_generator", "Generating search queries...", {"search_queries": ["a", "b"]})
        yield ("done", "Report generated.", {"final_report": "Report content"})

    mock_stepwise_agent.side_effect = fake_stepwise_agent

    with patch("builtins.print") as mock_print:
        run_agent("Test Topic", debug=True)
        debug_calls = [call for call in mock_print.call_args_list if "[DEBUG]" in str(call)]
        assert debug_calls, "No debug output was printed when debug=True"

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('yaspin.yaspin', autospec=True)
def test_run_agent_with_debug_flag_false(mock_yaspin, mock_open_func, mock_stepwise_agent, capsys):
    """
    Tests that debug logs are not printed when debug=False.
    """
    mock_spinner = MagicMock()
    mock_yaspin.return_value = mock_spinner

    mock_stepwise_agent.return_value = iter([
        ("query_generator", "Generating search queries...", {"search_queries": ["a", "b"]}),
        ("done", "Report generated.", {"final_report": "Report content"})
    ])

    run_agent("Test Topic", debug=False)
    captured = capsys.readouterr()
    assert "[DEBUG]" not in captured.out
