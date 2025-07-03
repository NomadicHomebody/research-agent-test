import sys
from workflow_builder import stepwise_agent
from yaspin import yaspin
from yaspin.spinners import Spinners

def run_agent(topic: str) -> None:
    """
    Runs the research agent for a given topic, providing spinner and status updates.

    Args:
        topic: The research topic.
    """
    report_path = "research_report.md"
    spinner = yaspin(Spinners.dots, text="Starting agent...")
    try:
        spinner.start()
        for node_name, status_message, state in stepwise_agent(topic):
            if node_name == "done":
                spinner.text = "Finalizing and writing report..."
                report = state.get("final_report", "")
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(report)
                spinner.ok("✅")
                print(f"\nReport generated: {report_path}\n")
                print(f"Open the report at: ./{report_path}")
                break
            else:
                spinner.text = status_message
    except Exception as e:
        spinner.fail("💥")
        print(f"\nError: {e}")
    finally:
        spinner.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent_runner.py \"<your research topic>\"")
        sys.exit(1)
    topic = sys.argv[1]
    run_agent(topic)
