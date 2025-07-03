import uuid
from langchain_core.messages import HumanMessage
from workflow_builder import build_workflow

def run_agent(topic: str):
    """
    Runs the research agent for a given topic.

    Args:
        topic: The research topic.
    """
    app = build_workflow()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    inputs = {"topic": topic, "messages": [HumanMessage(content=f"Start research on: {topic}")]}

    for output_chunk in app.stream(inputs, config=config, stream_mode="values"):
        print(f"--- Chunk ---")
        for key, value in output_chunk.items():
            print(f"{key}: {value}")

    final_state = app.get_state(config)
    report = final_state.values["final_report"]

    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    run_agent("The impact of AI on software development")
