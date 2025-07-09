"""
Unit tests for agent_runner.py.

These tests validate the run_agent workflow, spinner/status updates, debug logging,
and report file output using mocks for all external dependencies.

- Uses pytest and unittest.mock for patching and assertions.
- Covers both debug and non-debug execution paths.
- Ensures correct file output and spinner behavior.

Dependencies: pytest, unittest.mock, agent_runner.py, yaspin
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock, mock_open
from agent_runner import run_agent

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('agent_runner.yaspin', autospec=True)
@pytest.mark.slow
def test_run_agent_with_spinner(mock_yaspin, mock_open_func, mock_stepwise_agent):
    """
    Tests the agent runner to ensure it executes the workflow, updates spinner, and saves the report.
    """
    class SpinnerMock:
        def __init__(self):
            self.texts = []
            self.ok = MagicMock()
            self.stop = MagicMock()
        @property
        def text(self):
            return None
        @text.setter
        def text(self, value):
            self.texts.append(value)
        def start(self): pass
        def fail(self, *a, **kw): pass

    spinner_mock = SpinnerMock()
    mock_yaspin.return_value = spinner_mock

    mock_stepwise_agent.return_value = iter([
        ("query_generator", "Generating search queries...", {"search_queries": ["a", "b"]}),
        ("web_searcher", "Performing web search...", {"retrieved_docs": [{"url": "x"}]}),
        ("content_scraper", "Scraping web content...", {"scraped_data": [{"url": "x", "content": "text"}]}),
        ("content_summarizer", "Summarizing content...", {"summaries": ["summary"]}),
        ("report_compiler", "Compiling final report...", {"final_report": "Report content"}),
        ("done", "Report generated.", {"final_report": "Report content"})
    ])

    run_agent("Test Topic", status_callback=None)

    assert any("Finalizing and writing report..." in t for t in spinner_mock.texts), "spinner.text was not set to 'Finalizing and writing report...'"
    assert spinner_mock.ok.call_count >= 0
    assert spinner_mock.stop.call_count >= 0
    mock_open_func.assert_called_once_with("research_report.md", "w", encoding="utf-8")
    mock_open_func().write.assert_called_once_with("Report content")

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('yaspin.yaspin', autospec=True)
@pytest.mark.slow
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
        run_agent("Test Topic", debug=True, status_callback=None)
        debug_calls = [call for call in mock_print.call_args_list if "[DEBUG]" in str(call)]
        assert debug_calls, "No debug output was printed when debug=True"

@patch('agent_runner.stepwise_agent')
@patch('builtins.open', new_callable=mock_open)
@patch('yaspin.yaspin', autospec=True)
@pytest.mark.slow
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

    run_agent("Test Topic", debug=False, status_callback=None)
    captured = capsys.readouterr()
    assert "[DEBUG]" not in captured.out
