
import pytest
from unittest.mock import patch, MagicMock
import requests
from research_graph import scrape_content_node, ResearchState

# Mock response object for requests.get
class MockResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"{self.status_code} Client Error")

@pytest.fixture
def requests_get_mock():
    """Fixture to mock requests.get."""
    with patch('research_graph.requests.get') as mock_get:
        yield mock_get

def test_happy_path(requests_get_mock):
    """Tests successful scraping of a single valid URL."""
    html_content = "<html><body><main><h1>Title</h1><p>This is the main content.</p></main></body></html>"
    requests_get_mock.return_value = MockResponse(content=html_content.encode('utf-8'))

    state = {
        "retrieved_docs": [{"url": "http://example.com/main"}],
        "messages": []
    }
    result = scrape_content_node(state)

    assert not result["error_message"]
    assert len(result["scraped_data"]) == 1
    assert result["scraped_data"][0]["url"] == "http://example.com/main"
    assert "This is the main content." in result["scraped_data"][0]["content"]
    assert "Title" in result["scraped_data"][0]["content"]
    assert requests_get_mock.called

def test_no_documents_to_scrape():
    """Tests behavior when the retrieved_docs list is empty."""
    state = {"retrieved_docs": [], "messages": []}
    result = scrape_content_node(state)
    assert "No documents to scrape" in result["error_message"]
    assert result["scraped_data"] == []

def test_http_error(requests_get_mock):
    """Tests handling of an HTTP 404 Not Found error."""
    requests_get_mock.return_value = MockResponse(content="", status_code=404)
    
    state = {
        "retrieved_docs": [{"url": "http://example.com/notfound"}],
        "messages": []
    }
    result = scrape_content_node(state)

    assert not result["error_message"]
    assert len(result["scraped_data"]) == 0
    assert any("Failed to scrape" in msg['content'] for msg in result["messages"])

def test_request_exception(requests_get_mock):
    """Tests handling of a network-level exception."""
    import requests
    requests_get_mock.side_effect = requests.exceptions.Timeout("Connection timed out")

    state = {
        "retrieved_docs": [{"url": "http://example.com/timeout"}],
        "messages": []
    }
    result = scrape_content_node(state)

    assert not result["error_message"]
    assert len(result["scraped_data"]) == 0
    assert any("Failed to scrape" in msg['content'] for msg in result["messages"])

def test_script_and_style_removal(requests_get_mock):
    """Ensures that <script> and <style> tags are removed from the output."""
    html_content = """
    <html>
        <head><style>.red {color: red;}</style></head>
        <body>
            <p>Visible text.</p>
            <script>alert('hello');</script>
        </body>
    </html>
    """
    requests_get_mock.return_value = MockResponse(content=html_content.encode('utf-8'))

    state = {
        "retrieved_docs": [{"url": "http://example.com/script-style"}],
        "messages": []
    }
    result = scrape_content_node(state)

    assert len(result["scraped_data"]) == 1
    scraped_content = result["scraped_data"][0]["content"]
    assert "Visible text" in scraped_content
    assert "alert('hello')" not in scraped_content
    assert ".red {color: red;}" not in scraped_content

def test_content_extraction_from_article(requests_get_mock):
    """Tests that content is preferentially extracted from an <article> tag."""
    html_content = "<html><body><header>Ignore</header><article><h1>Article</h1><p>Main article text.</p></article><footer>Ignore</footer></body></html>"
    requests_get_mock.return_value = MockResponse(content=html_content.encode('utf-8'))

    state = {
        "retrieved_docs": [{"url": "http://example.com/article"}],
        "messages": []
    }
    result = scrape_content_node(state)
    
    assert len(result["scraped_data"]) == 1
    scraped_content = result["scraped_data"][0]["content"]
    assert "Main article text" in scraped_content
    assert "Ignore" not in scraped_content

if __name__ == "__main__":
    pytest.main([__file__])
