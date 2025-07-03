# AI Research Assistant

## Getting Started

Follow these steps to set up and run the AI Research Assistant locally:

### Prerequisites
1. **Python**: Ensure Python 3.8 or newer is installed.
2. **IDE**: Visual Studio Code is recommended.
3. **Internet Access**: Required for research tools and API access.

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv research_agent_env
   ```

3. **Activate the Virtual Environment**:
    - **Windows**:
        ```bash
        research_agent_env\Scripts\activate
        ```
    - **macOS/Linux**:
        ```bash
        source research_agent_env/bin/activate
        ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up API Keys**:
   - Open the `.env` file and add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     LANGCHAIN_TRACING_KEY=your_langchain_tracing_key_here
     ```

### Running the Application
1. **Run the Script**:
   ```bash
   python research_graph.py
   ```

2. **Provide a Research Topic**:
   - The application will prompt you to enter a topic for research.

3. **View the Output**:
   - The final research report will be saved as `research_report.md`.

### Running Unit Tests
To ensure the integrity and correctness of the codebase, run the unit tests.

- **To run all tests:**
  ```bash
  python -m unittest discover test
  ```

- **To run a specific test file:**
  ```bash
  python -m unittest test/test_file_name.py
  ```
  (Replace `test_file_name.py` with the actual name of the test file)

### Notes
- Ensure all API keys are valid and have the necessary permissions.
- For debugging and tracing, consider setting up LangSmith.