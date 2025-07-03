import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from research_graph import summarize_content_node, ResearchState

class TestSummarizeContentNode(unittest.TestCase):

    @patch('research_graph.call_llm')
    def test_summarize_content_happy_path(self, mock_call_llm):
        """Test happy path: valid scraped data returns summaries."""
        # Arrange
        mock_llm_response = MagicMock()
        mock_llm_response.content = "This is a summary."
        mock_call_llm.return_value = mock_llm_response

        state = ResearchState(
            topic="AI in healthcare",
            scraped_data=[
                {"url": "http://example.com/ai-healthcare", "content": "This is a long article about AI in healthcare..."},
                {"url": "http://example.com/another-article", "content": "Another long article..."}
            ],
            messages=[]
        )

        # Act
        result = summarize_content_node(state)

        # Assert
        self.assertIn('summaries', result)
        self.assertEqual(len(result['summaries']), 2)
        self.assertEqual(result['summaries'][0], "This is a summary.")
        self.assertEqual(mock_call_llm.call_count, 2)
        self.assertIn('Successfully summarized content', result['messages'][-1]['content'])

    def test_no_scraped_data(self):
        """Test edge case: no scraped data to summarize."""
        # Arrange
        state = ResearchState(
            topic="AI in healthcare",
            scraped_data=[],
            messages=[]
        )

        # Act
        result = summarize_content_node(state)

        # Assert
        self.assertEqual(len(result['summaries']), 0)
        self.assertIn("No scraped content available to summarize.", result['error_message'])

    def test_empty_content_in_scraped_data(self):
        """Test edge case: one of the documents has empty content."""
        # Arrange
        state = ResearchState(
            topic="AI in healthcare",
            scraped_data=[
                {"url": "http://example.com/empty", "content": ""},
                {"url": "http://example.com/valid", "content": "Valid content."}
            ],
            messages=[]
        )

        with patch('research_graph.call_llm') as mock_call_llm:
            mock_llm_response = MagicMock()
            mock_llm_response.content = "Summary of valid content."
            mock_call_llm.return_value = mock_llm_response

            # Act
            result = summarize_content_node(state)

            # Assert
            self.assertEqual(len(result['summaries']), 1)
            self.assertEqual(result['summaries'][0], "Summary of valid content.")
            mock_call_llm.assert_called_once() # Should only be called for the valid content
            self.assertIn("Skipping summarization for http://example.com/empty", result['messages'][0]['content'])

    @patch('research_graph.call_llm')
    def test_llm_error(self, mock_call_llm):
        """Test exception handling: LLM call fails."""
        # Arrange
        mock_call_llm.side_effect = Exception("LLM is down")
        state = ResearchState(
            topic="AI in healthcare",
            scraped_data=[{"url": "http://example.com/article", "content": "Some content..."}],
            messages=[]
        )

        # Act
        result = summarize_content_node(state)

        # Assert
        self.assertEqual(len(result['summaries']), 0)
        self.assertIn("Error summarizing content", result['messages'][-2]['content'])
        self.assertIn("Could not generate any summaries", result['error_message'])

    @patch('research_graph.call_llm')
    def test_llm_returns_empty_summary(self, mock_call_llm):
        """Test edge case: LLM returns an empty or whitespace-only summary."""
        # Arrange
        mock_llm_response = MagicMock()
        mock_llm_response.content = "   "
        mock_call_llm.return_value = mock_llm_response

        state = ResearchState(
            topic="AI",
            scraped_data=[{"url": "http://example.com/article", "content": "Some content..."}],
            messages=[]
        )

        # Act
        result = summarize_content_node(state)

        # Assert
        self.assertEqual(len(result['summaries']), 0)
        self.assertIn("LLM returned an empty summary", result['messages'][-2]['content'])
        self.assertIn("Could not generate any summaries", result['error_message'])

if __name__ == '__main__':
    unittest.main()
