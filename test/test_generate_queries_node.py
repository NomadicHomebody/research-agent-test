import os
import pytest
from dotenv import load_dotenv
from research_graph import generate_queries_node, ResearchState

# Ensure environment variables are loaded for LLM
load_dotenv()

def test_happy_path(monkeypatch):
    # Mock LLM response
    class MockLLMResponse:
        content = "1. What is AI?\n2. How does AI impact creative writing?\n3. Examples of AI tools for writers."

    def mock_llm_invoke(messages):
        return MockLLMResponse()

    import research_graph
    monkeypatch.setattr(research_graph, "call_llm", lambda messages: mock_llm_invoke(messages))

    state = {
        "topic": "AI and creative writing",
        "messages": []
    }
    result = generate_queries_node(state)
    assert isinstance(result["search_queries"], list)
    assert len(result["search_queries"]) >= 3
    assert all(isinstance(q, str) and q for q in result["search_queries"])
    assert result["error_message"] == ""

def test_empty_topic():
    state = {
        "topic": "",
        "messages": []
    }
    result = generate_queries_node(state)
    assert result["search_queries"] == []
    assert "Invalid topic" in result["error_message"]

def test_non_string_topic():
    state = {
        "topic": None,
        "messages": []
    }
    result = generate_queries_node(state)
    assert result["search_queries"] == []
    assert "Invalid topic" in result["error_message"]

def test_llm_exception(monkeypatch):
    def mock_llm_invoke(messages):
        raise RuntimeError("LLM failure")

    import research_graph
    monkeypatch.setattr(research_graph, "call_llm", lambda messages: mock_llm_invoke(messages))

    state = {
        "topic": "AI and creative writing",
        "messages": []
    }
    result = generate_queries_node(state)
    assert result["search_queries"] == []
    assert "Error generating queries" in result["error_message"]

def test_parsing_edge_case(monkeypatch):
    # LLM returns unnumbered lines
    class MockLLMResponse:
        content = "AI and writing\nCreative tools\nFuture trends"

    def mock_llm_invoke(messages):
        return MockLLMResponse()

    import research_graph
    monkeypatch.setattr(research_graph, "call_llm", lambda messages: mock_llm_invoke(messages))

    state = {
        "topic": "AI and creative writing",
        "messages": []
    }
    result = generate_queries_node(state)
    assert isinstance(result["search_queries"], list)
    assert len(result["search_queries"]) == 3
    assert result["error_message"] == ""

if __name__ == "__main__":
    pytest.main([__file__])