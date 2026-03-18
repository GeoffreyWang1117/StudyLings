# I AM NOT DONE

"""
Exercise: Checkpointing for Fault Tolerance

Checkpointing saves stream processing state periodically for fault recovery.
Enables exactly-once or at-least-once processing semantics.

Key concepts:
- Periodic state snapshots
- Coordinated checkpoints across operators
- Recovery from checkpoint
- Barrier-based synchronization

Your task: Implement checkpointing mechanism.
"""

from typing import Dict, Any
import time


class StatefulOperator:
    """Stateful stream operator with checkpointing"""

    def __init__(self, operator_id: str):
        self.operator_id = operator_id
        self.state = {}
        self.checkpoint_interval = 5.0
        self.last_checkpoint = time.time()

    def process(self, key: str, value: int):
        """Process event and update state"""
        # TODO: Process event
        # - Update state
        # - Check if checkpoint needed
        pass

    def checkpoint(self) -> Dict[str, Any]:
        """Create checkpoint of current state"""
        # TODO: Create checkpoint
        # - Return snapshot of state
        # - Update last_checkpoint time
        pass

    def restore(self, checkpoint: Dict[str, Any]):
        """Restore from checkpoint"""
        # TODO: Restore state from checkpoint
        pass

    def should_checkpoint(self) -> bool:
        """Check if checkpoint is needed"""
        # TODO: Check if enough time has passed
        pass


import unittest


class TestCheckpointing(unittest.TestCase):
    def test_checkpoint_restore(self):
        op = StatefulOperator("op1")
        op.process("key1", 10)
        op.process("key2", 20)

        checkpoint = op.checkpoint()

        op2 = StatefulOperator("op1")
        op2.restore(checkpoint)

        self.assertEqual(op2.state, op.state)


if __name__ == '__main__':
    unittest.main()
