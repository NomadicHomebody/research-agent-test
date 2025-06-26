import pytest
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from research_graph import web_search_node, ResearchState

# Load environment variables for Tavily API key
load_dotenv()

@pytest.fixture
def tavily_search_mock():
    """Fixture to mock the TavilySearchResults tool."""
    with patch('research_graph.TavilySearchResults') as mock:
        instance = mock.return_value
        instance.invoke = MagicMock()
        yield instance

def test_happy_path(tavily_search_mock):
    """Tests the normal, successful execution of the web_search_node."""
    # Mock the search results
    tavily_search_mock.invoke.return_value = [
        {'url': 'http://example.com/doc1', 'content': 'Content 1'},
        {'url': 'http://example.com/doc2', 'content': 'Content 2'}
    ]

    state = {
        "search_queries": ["query1", "query2"],
        "messages": []
    }

    result = web_search_node(state)

    assert not result["error_message"]
    assert len(result["retrieved_docs"]) == 2
    assert tavily_search_mock.invoke.call_count == 2

def test_empty_queries():
    """Tests behavior when the input list of search queries is empty."""
    state = {
        "search_queries": [],
        "messages": []
    }

    result = web_search_node(state)

    assert "No search queries provided" in result["error_message"]
    assert result["retrieved_docs"] == []

def test_deduplication(tavily_search_mock):
    """Ensures that duplicate documents (based on URL) are removed."""
    tavily_search_mock.invoke.side_effect = [
        [
            {'url': 'http://example.com/doc1', 'content': 'Content 1'},
            {'url': 'http://example.com/doc2', 'content': 'Content 2'}
        ],
        [
            {'url': 'http://example.com/doc1', 'content': 'Content 1, updated'},
            {'url': 'http://example.com/doc3', 'content': 'Content 3'}
        ]
    ]

    state = {
        "search_queries": ["query1", "query2"],
        "messages": []
    }

    result = web_search_node(state)

    assert len(result["retrieved_docs"]) == 3
    urls = {doc['url'] for doc in result["retrieved_docs"]}
    assert urls == {'http://example.com/doc1', 'http://example.com/doc2', 'http://example.com/doc3'}

def test_api_error(tavily_search_mock):
    """Tests how the node handles an exception from the search tool."""
    tavily_search_mock.invoke.side_effect = RuntimeError("API limit reached")

    state = {
        "search_queries": ["query1"],
        "messages": []
    }

    result = web_search_node(state)

    assert not result["error_message"]
    assert result["retrieved_docs"] == []
    assert any("Search failed for query" in msg['content'] for msg in result["messages"])

if __name__ == "__main__":
    pytest.main([__file__])
