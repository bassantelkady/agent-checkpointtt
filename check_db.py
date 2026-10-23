
from db_helpers import save_checkpoint, list_checkpoints

state = {
    "session_id": "list_test_001",
    "task_id": "task_001",
    "step_number": 1,
    "status": "done",
}

checkpoint_id = save_checkpoint(state)

checkpoints = list_checkpoints("list_test_001")

print("Checkpoint ID:", checkpoint_id)
print("Checkpoints:", checkpoints)

assert checkpoint_id in checkpoints

print("list_checkpoints test passed!")

