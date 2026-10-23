
from contextlib import contextmanager
from langgraph.checkpoint.sqlite import SqliteSaver


@contextmanager
def get_checkpointer(db_path="langgraph_checkpoints.db"):
    """Provide a LangGraph SQLite checkpointer."""
    with SqliteSaver.from_conn_string(db_path) as checkpointer:
        yield checkpointer
