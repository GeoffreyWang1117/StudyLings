# I AM NOT DONE

"""
dist04_raft_consensus.py

Raft is a consensus algorithm designed to be more understandable than Paxos
while providing the same guarantees. It's used in distributed systems to ensure
all nodes agree on a shared state.

Key components:
- Leader Election: One node is elected as leader to manage the log
- Log Replication: Leader receives client requests and replicates to followers
- Safety: Ensures committed entries are never lost

Your task: Implement simplified Raft leader election and log replication.

Key concepts:
- Terms: Logical clock that increments with each election
- States: Follower, Candidate, Leader
- Election timeout: Random timeout that triggers new election
- Heartbeat: Leader sends periodic heartbeats to maintain authority
- Log entries: Commands with term number and index
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import unittest


class NodeState(Enum):
    """Raft node states."""
    FOLLOWER = auto()
    CANDIDATE = auto()
    LEADER = auto()


@dataclass
class LogEntry:
    """A log entry in Raft."""
    term: int
    index: int
    command: str


class RaftNode:
    """A Raft node implementation."""

    def __init__(self, node_id: int, election_timeout: int):
        """Initialize a Raft node."""
        self.id = node_id
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.last_applied = 0

        # Leader-specific state
        self.next_index: Dict[int, int] = {}  # For each server, index of next log entry to send
        self.match_index: Dict[int, int] = {}  # For each server, index of highest log entry replicated

        # Election state
        self.votes_received: List[int] = []
        self.election_timeout = election_timeout
        self.time_since_heartbeat = 0

    def start_election(self, cluster_size: int):
        """
        TODO: Start a new election.

        - Increment current_term
        - Transition to Candidate state
        - Vote for self
        - Reset votes_received to just self
        - Reset time_since_heartbeat
        """
        pass  # TODO: Implement this

    def request_vote(self, candidate_id: int, candidate_term: int,
                     last_log_index: int, last_log_term: int) -> Tuple[bool, int]:
        """
        TODO: Handle RequestVote RPC.

        Grant vote if:
        1. candidate_term >= current_term
        2. Haven't voted for anyone else this term (or already voted for this candidate)
        3. Candidate's log is at least as up-to-date as receiver's log
           (compare last_log_term first, then last_log_index)

        If candidate_term > current_term:
        - Update current_term
        - Convert to Follower
        - Reset voted_for

        Return (vote_granted, current_term)
        """
        pass  # TODO: Implement this

    def receive_vote(self, voter_id: int, cluster_size: int) -> bool:
        """
        TODO: Record a vote and check if won election.

        - Add voter_id to votes_received (if not already present)
        - If received votes from majority of cluster, become Leader
        - Initialize next_index and match_index for all nodes
        - Return True if became leader
        """
        pass  # TODO: Implement this

    def append_entries(self, leader_term: int) -> bool:
        """
        TODO: Handle heartbeat/AppendEntries RPC (simplified - just heartbeat).

        - If leader_term < current_term, reject (return False)
        - If leader_term >= current_term:
          - Update current_term if necessary
          - Convert to Follower if not already
          - Reset voted_for if term changed
          - Reset time_since_heartbeat
          - Return True
        """
        pass  # TODO: Implement this

    def append_entry(self, command: str) -> Optional[int]:
        """
        TODO: Leader appends a new entry to its log.

        - Only works if this node is Leader
        - Create new LogEntry with current_term and next index
        - Add to log
        - Return the index of the new entry
        - Return None if not leader
        """
        pass  # TODO: Implement this

    def replicate_log_entry(self, follower_id: int, entry: LogEntry) -> bool:
        """
        TODO: Simulate log replication to a follower.

        - Only works if this node is Leader
        - Update next_index[follower_id] to entry.index + 1
        - Update match_index[follower_id] to entry.index
        - Return True if successful, False if not leader
        """
        pass  # TODO: Implement this

    def try_commit(self, cluster_size: int) -> bool:
        """
        TODO: Try to commit entries based on replication.

        - Only works if this node is Leader
        - Find highest index N where:
          1. N > commit_index
          2. Majority of match_index[i] >= N
          3. log[N-1].term == current_term (log is 0-indexed)
        - Update commit_index to N if found
        - Return True if commit_index was updated
        """
        pass  # TODO: Implement this

    def tick(self):
        """
        TODO: Advance time by 1 unit.

        - Increment time_since_heartbeat
        """
        pass  # TODO: Implement this

    def get_last_log_index(self) -> int:
        """Get the index of the last log entry."""
        return self.log[-1].index if self.log else 0

    def get_last_log_term(self) -> int:
        """Get the term of the last log entry."""
        return self.log[-1].term if self.log else 0

    def is_election_timeout(self) -> bool:
        """Check if election timeout has occurred."""
        return self.time_since_heartbeat >= self.election_timeout


# Unit Tests
class TestRaftConsensus(unittest.TestCase):

    def test_initial_state(self):
        node = RaftNode(1, 150)
        self.assertEqual(node.state, NodeState.FOLLOWER)
        self.assertEqual(node.current_term, 0)
        self.assertIsNone(node.voted_for)

    def test_start_election(self):
        node = RaftNode(1, 150)
        node.start_election(3)

        self.assertEqual(node.state, NodeState.CANDIDATE)
        self.assertEqual(node.current_term, 1)
        self.assertEqual(node.voted_for, 1)
        self.assertEqual(node.votes_received, [1])

    def test_request_vote_grant(self):
        node = RaftNode(1, 150)

        granted, term = node.request_vote(2, 1, 0, 0)

        self.assertTrue(granted)
        self.assertEqual(term, 1)
        self.assertEqual(node.voted_for, 2)
        self.assertEqual(node.current_term, 1)

    def test_request_vote_already_voted(self):
        node = RaftNode(1, 150)
        node.current_term = 1
        node.voted_for = 2

        # Different candidate, same term
        granted, _ = node.request_vote(3, 1, 0, 0)
        self.assertFalse(granted)

        # Same candidate, same term
        granted, _ = node.request_vote(2, 1, 0, 0)
        self.assertTrue(granted)

    def test_request_vote_old_term(self):
        node = RaftNode(1, 150)
        node.current_term = 5

        granted, term = node.request_vote(2, 3, 0, 0)

        self.assertFalse(granted)
        self.assertEqual(term, 5)

    def test_win_election(self):
        node = RaftNode(1, 150)
        node.start_election(3)

        # Node 1 already voted for itself
        self.assertEqual(node.state, NodeState.CANDIDATE)

        # Receive vote from node 2 (now have 2/3 - majority)
        won = node.receive_vote(2, 3)

        self.assertTrue(won)
        self.assertEqual(node.state, NodeState.LEADER)

    def test_election_needs_majority(self):
        node = RaftNode(1, 150)
        node.start_election(5)

        # Only 1/5 votes (self)
        self.assertEqual(node.state, NodeState.CANDIDATE)

        # 2/5 - not majority
        won = node.receive_vote(2, 5)
        self.assertFalse(won)
        self.assertEqual(node.state, NodeState.CANDIDATE)

        # 3/5 - majority!
        won = node.receive_vote(3, 5)
        self.assertTrue(won)
        self.assertEqual(node.state, NodeState.LEADER)

    def test_heartbeat_updates_follower(self):
        node = RaftNode(1, 150)
        node.current_term = 1
        node.time_since_heartbeat = 100

        accepted = node.append_entries(2)

        self.assertTrue(accepted)
        self.assertEqual(node.current_term, 2)
        self.assertEqual(node.state, NodeState.FOLLOWER)
        self.assertEqual(node.time_since_heartbeat, 0)

    def test_heartbeat_rejects_old_term(self):
        node = RaftNode(1, 150)
        node.current_term = 5

        accepted = node.append_entries(3)

        self.assertFalse(accepted)
        self.assertEqual(node.current_term, 5)  # Should not change

    def test_leader_append_entry(self):
        node = RaftNode(1, 150)
        node.state = NodeState.LEADER
        node.current_term = 1

        index = node.append_entry("SET x=1")

        self.assertEqual(index, 1)
        self.assertEqual(len(node.log), 1)
        self.assertEqual(node.log[0].term, 1)
        self.assertEqual(node.log[0].index, 1)
        self.assertEqual(node.log[0].command, "SET x=1")

    def test_follower_cannot_append_entry(self):
        node = RaftNode(1, 150)
        self.assertEqual(node.state, NodeState.FOLLOWER)

        index = node.append_entry("SET x=1")

        self.assertIsNone(index)
        self.assertEqual(len(node.log), 0)

    def test_log_replication(self):
        leader = RaftNode(1, 150)
        leader.state = NodeState.LEADER
        leader.current_term = 1
        leader.next_index[2] = 1
        leader.match_index[2] = 0

        index = leader.append_entry("SET x=1")
        entry = leader.log[0]

        success = leader.replicate_log_entry(2, entry)

        self.assertTrue(success)
        self.assertEqual(leader.next_index[2], 2)
        self.assertEqual(leader.match_index[2], 1)

    def test_commit_with_majority(self):
        leader = RaftNode(1, 150)
        leader.state = NodeState.LEADER
        leader.current_term = 1

        # Leader has entry at index 1
        leader.append_entry("SET x=1")

        # Initialize for 3-node cluster
        leader.next_index[2] = 1
        leader.next_index[3] = 1
        leader.match_index[1] = 1  # Leader itself
        leader.match_index[2] = 0
        leader.match_index[3] = 0

        # Replicate to node 2
        leader.replicate_log_entry(2, leader.log[0])

        # Now 2/3 nodes have the entry (leader + node 2)
        committed = leader.try_commit(3)

        self.assertTrue(committed)
        self.assertEqual(leader.commit_index, 1)

    def test_election_timeout_tick(self):
        node = RaftNode(1, 150)

        for _ in range(149):
            node.tick()
            self.assertFalse(node.is_election_timeout())

        node.tick()
        self.assertTrue(node.is_election_timeout())

    def test_candidate_converts_to_follower_on_higher_term(self):
        node = RaftNode(1, 150)
        node.start_election(3)
        self.assertEqual(node.state, NodeState.CANDIDATE)
        self.assertEqual(node.current_term, 1)

        # Receive heartbeat from leader with higher term
        node.append_entries(2)

        self.assertEqual(node.state, NodeState.FOLLOWER)
        self.assertEqual(node.current_term, 2)


if __name__ == '__main__':
    unittest.main()
