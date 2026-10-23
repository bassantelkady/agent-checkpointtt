
import sqlite3

from typing import Optional

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


def init_db(path="agent.db"):
    """Create the SQLite database and its tables if they don't exist."""
    db_path = Path(path)

    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema)

    return str(db_path)



import json
import uuid
from datetime import datetime, timezone


def save_checkpoint(state: dict) -> str:
    """Save an AgentState dictionary and return its checkpoint ID."""
    if not isinstance(state, dict):
        raise TypeError("state must be a dictionary")

    checkpoint_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    session_id = state.get("session_id")
    task_id = state.get("task_id")
    step_number = state.get("step_number", 0)

    with sqlite3.connect(init_db()) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            """
            INSERT INTO checkpoints (
                checkpoint_id,
                session_id,
                task_id,
                step_number,
                agent_state_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                checkpoint_id,
                session_id,
                task_id,
                step_number,
                json.dumps(state, ensure_ascii=False),
                created_at,
            ),
        )

    return checkpoint_id


def load_checkpoint(checkpoint_id: str) -> dict:
    """Load an AgentState dictionary by checkpoint ID."""
    with sqlite3.connect(init_db()) as conn:
        row = conn.execute(
            """
            SELECT agent_state_json
            FROM checkpoints
            WHERE checkpoint_id = ?
            """,
            (checkpoint_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"Checkpoint not found: {checkpoint_id}")

    return json.loads(row[0])


def get_last_checkpoint(session_id: str) -> Optional[dict]:
    """Return the latest saved state for a session, or None."""
    with sqlite3.connect(init_db()) as conn:
        row = conn.execute(
            """
            SELECT agent_state_json
            FROM checkpoints
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (session_id,),
        ).fetchone()

    if row is None:
        return None

    return json.loads(row[0])




def list_checkpoints(session_id: str) -> list[str]:
    """Return checkpoint IDs belonging to a session."""
    with sqlite3.connect(init_db()) as conn:
        rows = conn.execute(
            """
            SELECT checkpoint_id
            FROM checkpoints
            WHERE session_id = ?
            ORDER BY created_at ASC
            """,
            (session_id,),
        ).fetchall()

    return [row[0] for row in rows]
