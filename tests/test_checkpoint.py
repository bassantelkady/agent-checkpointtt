
import uuid

from db_helpers import (
    save_checkpoint,
    load_checkpoint,
    get_last_checkpoint,
)


def test_save_and_load_checkpoint():
    state = {
        "session_id": "test_" + str(uuid.uuid4()),
        "task_id": "task_001",
        "step_number": 1,
        "status": "done",
    }

    checkpoint_id = save_checkpoint(state)
    loaded_state = load_checkpoint(checkpoint_id)

    assert loaded_state == state


def test_get_last_checkpoint():
    session_id = "test_" + str(uuid.uuid4())

    state = {
        "session_id": session_id,
        "task_id": "task_002",
        "step_number": 2,
        "status": "done",
    }

    save_checkpoint(state)

    last_state = get_last_checkpoint(session_id)

    assert last_state == state


def test_missing_session_returns_none():
    session_id = "missing_" + str(uuid.uuid4())

    result = get_last_checkpoint(session_id)

    assert result is None
