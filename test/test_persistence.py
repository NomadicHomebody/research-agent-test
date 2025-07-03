import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from workflow_builder import build_workflow

@patch('workflow_builder.MemorySaver')
def test_build_workflow_with_persistence(mock_memory_saver):
    """
    Tests that the workflow is built with persistence.
    """
    # Mock the checkpointer
    mock_checkpointer = MagicMock()
    mock_memory_saver.return_value = mock_checkpointer

    # Build the workflow
    app = build_workflow()

    # Assert that the checkpointer was created and the app was compiled with it
    mock_memory_saver.assert_called_once_with()
    assert app.checkpointer == mock_checkpointer
