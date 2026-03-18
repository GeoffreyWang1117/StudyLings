# I AM NOT DONE

"""
dist10_two_phase_commit.py

Two-Phase Commit (2PC) is a distributed algorithm that ensures all participants
in a distributed transaction either commit or abort together. It's crucial for
maintaining ACID properties across distributed databases.

Protocol phases:
1. Prepare Phase: Coordinator asks all participants to prepare (vote yes/no)
2. Commit Phase: If all vote yes, coordinator tells all to commit; otherwise abort

Your task: Implement the Two-Phase Commit protocol with coordinator and participants.

Key concepts:
- Coordinator: Orchestrates the transaction
- Participants: Nodes that execute parts of the transaction
- Prepare: Participant locks resources and votes
- Commit/Abort: Final decision applied atomically
- Blocking: Protocol blocks if coordinator fails (limitation of 2PC)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional
import unittest


class Vote(Enum):
    """Vote types."""
    YES = auto()
    NO = auto()


class ParticipantState(Enum):
    """Participant states."""
    IDLE = auto()
    PREPARED = auto()
    COMMITTED = auto()
    ABORTED = auto()


class CoordinatorState(Enum):
    """Coordinator states."""
    IDLE = auto()
    PREPARING = auto()
    COMMITTING = auto()
    ABORTING = auto()
    COMMITTED = auto()
    ABORTED = auto()


class TransactionResult(Enum):
    """Transaction result."""
    COMMITTED = auto()
    ABORTED = auto()
    IN_PROGRESS = auto()


@dataclass
class Transaction:
    """A distributed transaction."""
    id: int
    operations: List[str]


class Participant:
    """A participant in 2PC."""

    def __init__(self, participant_id: int):
        """Initialize a participant."""
        self.id = participant_id
        self.state = ParticipantState.IDLE
        self.prepared_transactions: Dict[int, Transaction] = {}
        self.committed_transactions: Dict[int, Transaction] = {}
        self.vote_to_abort = False  # Simulates failures

    def prepare(self, transaction: Transaction) -> Vote:
        """
        TODO: Handle prepare request.

        - If vote_to_abort is True, return Vote.NO
        - Otherwise, store transaction in prepared_transactions
        - Change state to PREPARED
        - Return Vote.YES
        """
        pass  # TODO: Implement this

    def commit(self, transaction_id: int) -> bool:
        """
        TODO: Handle commit request.

        - Must be in PREPARED state
        - Move transaction from prepared_transactions to committed_transactions
        - Change state to COMMITTED
        - Return True if successful, False otherwise
        """
        pass  # TODO: Implement this

    def abort(self, transaction_id: int) -> bool:
        """
        TODO: Handle abort request.

        - Remove transaction from prepared_transactions
        - Change state to ABORTED
        - Return True
        """
        pass  # TODO: Implement this

    def set_vote_to_abort(self, should_abort: bool):
        """Set whether this participant will vote to abort."""
        self.vote_to_abort = should_abort

    def is_transaction_committed(self, transaction_id: int) -> bool:
        """Check if a transaction is committed."""
        return transaction_id in self.committed_transactions

    def reset(self):
        """Reset to idle state."""
        self.state = ParticipantState.IDLE


class Coordinator:
    """The coordinator in 2PC."""

    def __init__(self):
        """Initialize a coordinator."""
        self.state = CoordinatorState.IDLE
        self.transaction: Optional[Transaction] = None
        self.votes: Dict[int, Vote] = {}
        self.participants: List[int] = []

    def add_participant(self, participant_id: int):
        """Add a participant."""
        self.participants.append(participant_id)

    def start_transaction(self, transaction: Transaction):
        """
        TODO: Start a new transaction.

        - Store the transaction
        - Clear votes
        - Change state to PREPARING
        """
        pass  # TODO: Implement this

    def receive_vote(self, participant_id: int, vote: Vote):
        """
        TODO: Record a vote from a participant.

        - Store the vote in votes dict
        """
        pass  # TODO: Implement this

    def has_all_votes(self) -> bool:
        """
        TODO: Check if all participants have voted.

        - Compare len(votes) with len(participants)
        """
        pass  # TODO: Implement this

    def should_commit(self) -> bool:
        """
        TODO: Determine if transaction should commit.

        - All votes must be YES
        - Return False if any vote is NO or not all votes received
        """
        pass  # TODO: Implement this

    def decide(self) -> TransactionResult:
        """
        TODO: Make commit/abort decision.

        - Must have all votes
        - If should_commit(), change state to COMMITTING, return COMMITTED
        - Otherwise, change state to ABORTING, return ABORTED
        - If not all votes, return IN_PROGRESS
        """
        pass  # TODO: Implement this

    def finalize_commit(self):
        """Finalize the commit."""
        self.state = CoordinatorState.COMMITTED

    def finalize_abort(self):
        """Finalize the abort."""
        self.state = CoordinatorState.ABORTED

    def reset(self):
        """Reset to idle state."""
        self.state = CoordinatorState.IDLE
        self.transaction = None
        self.votes.clear()


class TwoPhaseCommitSystem:
    """A complete 2PC system."""

    def __init__(self):
        """Initialize the system."""
        self.coordinator = Coordinator()
        self.participants: Dict[int, Participant] = {}
        self.transaction_counter = 0

    def add_participant(self, participant_id: int):
        """Add a participant to the system."""
        self.participants[participant_id] = Participant(participant_id)
        self.coordinator.add_participant(participant_id)

    def set_participant_vote(self, participant_id: int, vote_to_abort: bool):
        """Set whether a participant will vote to abort."""
        participant = self.participants.get(participant_id)
        if participant:
            participant.set_vote_to_abort(vote_to_abort)

    def execute_transaction(self, operations: List[str]) -> TransactionResult:
        """
        TODO: Execute a complete 2PC transaction.

        Phase 1: Prepare
        - Create transaction with next transaction_id
        - Start transaction on coordinator
        - Send prepare to all participants
        - Collect votes and send to coordinator

        Phase 2: Commit or Abort
        - Coordinator decides based on votes
        - If COMMITTED: send commit to all participants
        - If ABORTED: send abort to all participants
        - Finalize coordinator state
        - Return result
        """
        pass  # TODO: Implement this

    def phase1_prepare(self, transaction: Transaction) -> Dict[int, Vote]:
        """
        TODO: Execute Phase 1 (Prepare).

        - For each participant, call prepare
        - Collect and return all votes
        """
        pass  # TODO: Implement this

    def phase2_commit(self, transaction_id: int):
        """
        TODO: Execute Phase 2 Commit.

        - For each participant, call commit
        - Finalize coordinator
        """
        pass  # TODO: Implement this

    def phase2_abort(self, transaction_id: int):
        """
        TODO: Execute Phase 2 Abort.

        - For each participant, call abort
        - Finalize coordinator
        """
        pass  # TODO: Implement this

    def get_coordinator_state(self) -> CoordinatorState:
        """Get coordinator state."""
        return self.coordinator.state

    def get_participant_state(self, participant_id: int) -> Optional[ParticipantState]:
        """Get participant state."""
        participant = self.participants.get(participant_id)
        return participant.state if participant else None

    def is_transaction_committed(self, transaction_id: int) -> bool:
        """Check if all participants have committed the transaction."""
        return all(
            p.is_transaction_committed(transaction_id)
            for p in self.participants.values()
        )

    def reset_all(self):
        """Reset all components."""
        self.coordinator.reset()
        for participant in self.participants.values():
            participant.reset()


# Unit Tests
class TestTwoPhaseCommit(unittest.TestCase):

    def test_participant_prepare_yes(self):
        participant = Participant(1)
        tx = Transaction(1, ["INSERT INTO table"])

        vote = participant.prepare(tx)

        self.assertEqual(vote, Vote.YES)
        self.assertEqual(participant.state, ParticipantState.PREPARED)
        self.assertIn(1, participant.prepared_transactions)

    def test_participant_prepare_no(self):
        participant = Participant(1)
        participant.set_vote_to_abort(True)

        tx = Transaction(1, ["INSERT INTO table"])
        vote = participant.prepare(tx)

        self.assertEqual(vote, Vote.NO)

    def test_participant_commit(self):
        participant = Participant(1)
        tx = Transaction(1, ["INSERT INTO table"])

        participant.prepare(tx)
        success = participant.commit(1)

        self.assertTrue(success)
        self.assertEqual(participant.state, ParticipantState.COMMITTED)
        self.assertTrue(participant.is_transaction_committed(1))
        self.assertNotIn(1, participant.prepared_transactions)

    def test_participant_abort(self):
        participant = Participant(1)
        tx = Transaction(1, ["INSERT INTO table"])

        participant.prepare(tx)
        success = participant.abort(1)

        self.assertTrue(success)
        self.assertEqual(participant.state, ParticipantState.ABORTED)
        self.assertNotIn(1, participant.prepared_transactions)

    def test_coordinator_all_yes_votes(self):
        coordinator = Coordinator()
        coordinator.add_participant(1)
        coordinator.add_participant(2)

        tx = Transaction(1, ["UPDATE table"])
        coordinator.start_transaction(tx)

        coordinator.receive_vote(1, Vote.YES)
        coordinator.receive_vote(2, Vote.YES)

        self.assertTrue(coordinator.has_all_votes())
        self.assertTrue(coordinator.should_commit())

    def test_coordinator_one_no_vote(self):
        coordinator = Coordinator()
        coordinator.add_participant(1)
        coordinator.add_participant(2)

        tx = Transaction(1, ["UPDATE table"])
        coordinator.start_transaction(tx)

        coordinator.receive_vote(1, Vote.YES)
        coordinator.receive_vote(2, Vote.NO)

        self.assertTrue(coordinator.has_all_votes())
        self.assertFalse(coordinator.should_commit())

    def test_coordinator_decide_commit(self):
        coordinator = Coordinator()
        coordinator.add_participant(1)
        coordinator.add_participant(2)

        tx = Transaction(1, ["UPDATE table"])
        coordinator.start_transaction(tx)

        coordinator.receive_vote(1, Vote.YES)
        coordinator.receive_vote(2, Vote.YES)

        result = coordinator.decide()
        self.assertEqual(result, TransactionResult.COMMITTED)
        self.assertEqual(coordinator.state, CoordinatorState.COMMITTING)

    def test_coordinator_decide_abort(self):
        coordinator = Coordinator()
        coordinator.add_participant(1)

        tx = Transaction(1, ["UPDATE table"])
        coordinator.start_transaction(tx)

        coordinator.receive_vote(1, Vote.NO)

        result = coordinator.decide()
        self.assertEqual(result, TransactionResult.ABORTED)
        self.assertEqual(coordinator.state, CoordinatorState.ABORTING)

    def test_full_commit_transaction(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)
        system.add_participant(3)

        result = system.execute_transaction([
            "INSERT INTO users VALUES (1, 'Alice')",
            "INSERT INTO accounts VALUES (1, 100)",
        ])

        self.assertEqual(result, TransactionResult.COMMITTED)
        self.assertEqual(system.get_coordinator_state(), CoordinatorState.COMMITTED)

        # All participants should have committed
        for i in [1, 2, 3]:
            self.assertEqual(system.get_participant_state(i), ParticipantState.COMMITTED)

    def test_abort_due_to_participant_failure(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)
        system.add_participant(3)

        # Participant 2 will vote to abort
        system.set_participant_vote(2, True)

        result = system.execute_transaction(["INSERT INTO users VALUES (1, 'Bob')"])

        self.assertEqual(result, TransactionResult.ABORTED)
        self.assertEqual(system.get_coordinator_state(), CoordinatorState.ABORTED)

        # All participants should have aborted
        for i in [1, 2, 3]:
            self.assertEqual(system.get_participant_state(i), ParticipantState.ABORTED)

    def test_phase1_prepare(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)

        tx = Transaction(1, ["UPDATE table"])
        votes = system.phase1_prepare(tx)

        self.assertEqual(len(votes), 2)
        self.assertEqual(votes.get(1), Vote.YES)
        self.assertEqual(votes.get(2), Vote.YES)

    def test_atomicity_all_or_nothing(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)

        system.set_participant_vote(1, True)  # Will abort

        system.execute_transaction(["UPDATE table"])

        # Neither participant should have committed
        self.assertFalse(system.is_transaction_committed(1))

    def test_multiple_transactions(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)

        result1 = system.execute_transaction(["TX1"])
        self.assertEqual(result1, TransactionResult.COMMITTED)

        system.reset_all()

        result2 = system.execute_transaction(["TX2"])
        self.assertEqual(result2, TransactionResult.COMMITTED)

    def test_single_participant(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)

        result = system.execute_transaction(["SINGLE OP"])
        self.assertEqual(result, TransactionResult.COMMITTED)

    def test_all_participants_vote_no(self):
        system = TwoPhaseCommitSystem()
        system.add_participant(1)
        system.add_participant(2)

        system.set_participant_vote(1, True)
        system.set_participant_vote(2, True)

        result = system.execute_transaction(["UPDATE"])
        self.assertEqual(result, TransactionResult.ABORTED)


if __name__ == '__main__':
    unittest.main()
