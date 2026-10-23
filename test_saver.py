

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from sqlite_saver import get_checkpointer


class AgentState(TypedDict):
    message: str


def test_checkpoint():
    builder = StateGraph(AgentState)

    def process(state: AgentState) -> AgentState:
        return {"message": state["message"] + " - saved"}

    builder.add_node("process", process)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)

    with get_checkpointer() as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)

        config = {
            "configurable": {
                "thread_id": "test_thread_001"
            }
        }

        result = graph.invoke(
            {"message": "Hello"},
            config=config
        )

        print("Graph result:", result)

        saved = graph.get_state(config)
        print("Saved checkpoint:", saved.values)

        assert saved.values["message"] == "Hello - saved"

    print("LangGraph checkpoint test passed!")


if __name__ == "__main__":
    test_checkpoint()
