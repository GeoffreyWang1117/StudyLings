# I AM NOT DONE

"""
dist05_paxos.py

Paxos is a family of protocols for solving consensus in a network of unreliable
processors. It's fundamental to distributed systems but known for being difficult
to understand and implement.

Basic Paxos has two phases:
- Phase 1 (Prepare): Proposer asks acceptors to promise not to accept older proposals
- Phase 2 (Accept): If majority promises, proposer asks acceptors to accept value

Your task: Implement Basic Paxos (single-decree).

Key concepts:
- Proposal numbers: Unique, totally-ordered identifiers
- Quorum: Majority of acceptors must agree
- Promise: Acceptor's commitment to ignore older proposals
- Chosen value: Value accepted by majority of acceptors
- Safety: Only one value can be chosen
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import unittest


@dataclass
class Proposal:
    """A Paxos proposal."""
    number: int  # Unique proposal number (higher = newer)
    value: str


@dataclass
class Promise:
    """A promise from an acceptor."""
    proposal_number: int
    accepted_proposal: Optional[Proposal]  # Previously accepted proposal, if any


class Phase(Enum):
    """Proposer phases."""
    IDLE = auto()
    PREPARE = auto()
    ACCEPT = auto()
    DECIDED = auto()


class Proposer:
    """A Paxos proposer."""

    def __init__(self, proposer_id: int):
        """Initialize a proposer."""
        self.id = proposer_id
        self.proposal_number = proposer_id  # Start with ID to ensure uniqueness
        self.proposed_value: Optional[str] = None
        self.promises_received: Dict[int, Promise] = {}
        self.accepts_received: List[int] = []
        self.phase = Phase.IDLE
        self.decided_value: Optional[str] = None

    def prepare(self, value: str, cluster_size: int) -> int:
        """
        TODO: Start Phase 1 (Prepare).

        - Generate new proposal number (increment by cluster_size to maintain uniqueness)
        - Store the value we want to propose
        - Clear promises_received and accepts_received
        - Set phase to Prepare
        - Return the proposal number
        """
        pass  # TODO: Implement this

    def receive_promise(self, acceptor_id: int, promise: Promise, cluster_size: int) -> bool:
        """
        TODO: Handle a Promise response from an acceptor.

        - Store the promise
        - If received promises from majority:
          - Check if any promise includes a previously accepted value
          - If so, must propose the value from the highest-numbered accepted proposal
          - Set phase to Accept
          - Return True (ready for Phase 2)
        - Otherwise return False (need more promises)
        """
        pass  # TODO: Implement this

    def receive_accept(self, acceptor_id: int, cluster_size: int) -> bool:
        """
        TODO: Handle an Accept response from an acceptor.

        - Record the acceptance
        - If received accepts from majority:
          - Set decided_value to the proposed value
          - Set phase to Decided
          - Return True (consensus reached!)
        - Otherwise return False (need more accepts)
        """
        pass  # TODO: Implement this

    def get_value_to_propose(self) -> Optional[str]:
        """Get the value to propose."""
        return self.proposed_value

    def is_decided(self) -> bool:
        """Check if consensus has been reached."""
        return self.phase == Phase.DECIDED


class Acceptor:
    """A Paxos acceptor."""

    def __init__(self, acceptor_id: int):
        """Initialize an acceptor."""
        self.id = acceptor_id
        self.promised_number: Optional[int] = None  # Highest proposal number promised
        self.accepted_proposal: Optional[Proposal] = None  # Highest-numbered proposal accepted

    def receive_prepare(self, proposal_number: int) -> Optional[Promise]:
        """
        TODO: Handle a Prepare request.

        - If proposal_number > promised_number (or no promise yet):
          - Update promised_number to proposal_number
          - Return Promise with proposal_number and accepted_proposal (if any)
        - Otherwise, reject (return None)
        """
        pass  # TODO: Implement this

    def receive_accept_request(self, proposal: Proposal) -> bool:
        """
        TODO: Handle an Accept request.

        - If no promise yet, or proposal.number >= promised_number:
          - Update promised_number to proposal.number
          - Update accepted_proposal to this proposal
          - Return True (accepted)
        - Otherwise, reject (return False)
        """
        pass  # TODO: Implement this

    def get_accepted_value(self) -> Optional[str]:
        """Get the accepted value."""
        return self.accepted_proposal.value if self.accepted_proposal else None


class PaxosCluster:
    """A Paxos cluster with proposers and acceptors."""

    def __init__(self, num_acceptors: int):
        """Initialize a Paxos cluster."""
        self.proposers: Dict[int, Proposer] = {}
        self.acceptors: Dict[int, Acceptor] = {
            i: Acceptor(i) for i in range(num_acceptors)
        }

    def add_proposer(self, proposer_id: int) -> Proposer:
        """Add a proposer to the cluster."""
        self.proposers[proposer_id] = Proposer(proposer_id)
        return self.proposers[proposer_id]

    def get_proposer(self, proposer_id: int) -> Optional[Proposer]:
        """Get a proposer by ID."""
        return self.proposers.get(proposer_id)

    def get_proposer_mut(self, proposer_id: int) -> Optional[Proposer]:
        """Get a mutable proposer by ID."""
        return self.proposers.get(proposer_id)

    def get_acceptor(self, acceptor_id: int) -> Optional[Acceptor]:
        """Get an acceptor by ID."""
        return self.acceptors.get(acceptor_id)

    def cluster_size(self) -> int:
        """Get the number of acceptors."""
        return len(self.acceptors)

    def phase1_prepare(self, proposer_id: int, value: str) -> List[Tuple[int, Optional[Promise]]]:
        """
        TODO: Execute Phase 1 for a proposer.

        - Call prepare on proposer
        - Send prepare to all acceptors
        - Collect promises
        - Return list of (acceptor_id, promise)
        """
        pass  # TODO: Implement this

    def phase2_accept(self, proposer_id: int) -> List[Tuple[int, bool]]:
        """
        TODO: Execute Phase 2 for a proposer.

        - Get the value to propose from proposer
        - Create proposal with proposer's proposal_number
        - Send accept request to all acceptors
        - Return list of (acceptor_id, accepted)
        """
        pass  # TODO: Implement this

    def run_paxos(self, proposer_id: int, value: str) -> Optional[str]:
        """
        TODO: Run full Paxos protocol for a proposer.

        - Execute Phase 1
        - Process promises
        - If got majority, execute Phase 2
        - Process accepts
        - Return decided value if consensus reached
        """
        pass  # TODO: Implement this

    def get_consensus_value(self) -> Optional[str]:
        """Check if any proposer has reached consensus."""
        for proposer in self.proposers.values():
            if proposer.is_decided():
                return proposer.decided_value
        return None


# Unit Tests
class TestPaxos(unittest.TestCase):

    def test_acceptor_promise(self):
        acceptor = Acceptor(0)

        promise = acceptor.receive_prepare(10)
        self.assertIsNotNone(promise)
        self.assertEqual(promise.proposal_number, 10)
        self.assertEqual(acceptor.promised_number, 10)

    def test_acceptor_rejects_old_prepare(self):
        acceptor = Acceptor(0)
        acceptor.receive_prepare(10)

        promise = acceptor.receive_prepare(5)
        self.assertIsNone(promise)
        self.assertEqual(acceptor.promised_number, 10)  # Should not change

    def test_acceptor_accept(self):
        acceptor = Acceptor(0)
        acceptor.receive_prepare(10)

        proposal = Proposal(10, "value1")
        accepted = acceptor.receive_accept_request(proposal)

        self.assertTrue(accepted)
        self.assertEqual(acceptor.accepted_proposal, proposal)

    def test_acceptor_rejects_old_accept(self):
        acceptor = Acceptor(0)
        acceptor.receive_prepare(10)

        proposal = Proposal(5, "value1")
        accepted = acceptor.receive_accept_request(proposal)

        self.assertFalse(accepted)
        self.assertIsNone(acceptor.accepted_proposal)

    def test_proposer_prepare_phase(self):
        proposer = Proposer(0)
        proposal_num = proposer.prepare("value1", 5)

        self.assertEqual(proposal_num, 5)  # 0 + 5
        self.assertEqual(proposer.phase, Phase.PREPARE)
        self.assertEqual(proposer.get_value_to_propose(), "value1")

    def test_proposer_receives_majority_promises(self):
        proposer = Proposer(0)
        proposer.prepare("value1", 5)

        # Receive promises from 3 out of 5 acceptors
        ready = proposer.receive_promise(0, Promise(5, None), 5)
        self.assertFalse(ready)

        ready = proposer.receive_promise(1, Promise(5, None), 5)
        self.assertFalse(ready)

        ready = proposer.receive_promise(2, Promise(5, None), 5)
        self.assertTrue(ready)  # Now have majority (3/5)
        self.assertEqual(proposer.phase, Phase.ACCEPT)

    def test_proposer_must_use_accepted_value(self):
        proposer = Proposer(0)
        proposer.prepare("value1", 5)

        # Acceptor 0 has previously accepted a different value
        old_proposal = Proposal(3, "old_value")
        proposer.receive_promise(0, Promise(5, old_proposal), 3)

        # Acceptor 1 has no previous acceptance
        proposer.receive_promise(1, Promise(5, None), 3)

        # Should now use "old_value" instead of "value1"
        self.assertEqual(proposer.get_value_to_propose(), "old_value")

    def test_proposer_uses_highest_accepted_value(self):
        proposer = Proposer(0)
        proposer.prepare("value1", 5)

        # Two acceptors with different accepted values
        proposer.receive_promise(0, Promise(5, Proposal(2, "value_a")), 3)
        proposer.receive_promise(1, Promise(5, Proposal(4, "value_b")), 3)

        # Should use value from highest-numbered proposal (4 > 2)
        self.assertEqual(proposer.get_value_to_propose(), "value_b")

    def test_full_paxos_single_proposer(self):
        cluster = PaxosCluster(3)
        cluster.add_proposer(0)

        result = cluster.run_paxos(0, "my_value")

        self.assertEqual(result, "my_value")
        self.assertTrue(cluster.get_proposer(0).is_decided())

    def test_acceptor_updates_promise(self):
        acceptor = Acceptor(0)

        acceptor.receive_prepare(10)
        self.assertEqual(acceptor.promised_number, 10)

        acceptor.receive_prepare(20)
        self.assertEqual(acceptor.promised_number, 20)

    def test_promise_includes_accepted_proposal(self):
        acceptor = Acceptor(0)

        acceptor.receive_prepare(10)
        acceptor.receive_accept_request(Proposal(10, "value1"))

        promise = acceptor.receive_prepare(20)
        self.assertEqual(promise.proposal_number, 20)
        self.assertEqual(promise.accepted_proposal, Proposal(10, "value1"))

    def test_consensus_reached(self):
        cluster = PaxosCluster(5)
        cluster.add_proposer(0)

        cluster.run_paxos(0, "consensus_value")

        # Check that majority of acceptors accepted the value
        count = 0
        for i in range(5):
            acceptor = cluster.get_acceptor(i)
            if acceptor and acceptor.get_accepted_value() == "consensus_value":
                count += 1

        self.assertGreaterEqual(count, 3)  # Majority of 5

    def test_proposal_number_uniqueness(self):
        proposer1 = Proposer(0)
        proposer2 = Proposer(1)
        proposer3 = Proposer(2)

        # With cluster_size 3, proposals will be 0+3=3, 1+3=4, 2+3=5
        self.assertEqual(proposer1.proposal_number, 0)
        self.assertEqual(proposer2.proposal_number, 1)
        self.assertEqual(proposer3.proposal_number, 2)


if __name__ == '__main__':
    unittest.main()
