# I AM NOT DONE

"""
os07_banker_algorithm.py

The Banker's Algorithm is a deadlock avoidance algorithm that tests for safety by
simulating the allocation of predetermined maximum possible amounts of all resources,
and then makes a "safe state" check to test for possible deadlock conditions.

Your task: Implement the Banker's Algorithm for deadlock avoidance.
"""

from typing import List, Optional
import unittest


class BankerAlgorithm:
    """Banker's Algorithm for deadlock avoidance."""

    def __init__(self, num_processes: int, num_resources: int,
                 available: List[int], maximum: List[List[int]]):
        """
        TODO: Initialize the Banker's Algorithm.

        Steps:
        1. Create allocation matrix (all zeros initially)
        2. Calculate need matrix: Need[i][j] = Maximum[i][j] - Allocation[i][j]

        Args:
            num_processes: Number of processes
            num_resources: Number of resource types
            available: Available[j] = number of available instances of resource j
            maximum: Maximum[i][j] = maximum demand of process i for resource j
        """
        pass  # TODO: Implement this

    def request_resources(self, process_id: int, request: List[int]) -> bool:
        """
        TODO: Process a resource request.

        Steps:
        1. Check if request <= need[process_id]
        2. Check if request <= available
        3. Pretend to allocate resources
        4. Check if state is safe
        5. If safe, commit the allocation; otherwise, rollback

        Args:
            process_id: Process requesting resources
            request: Requested resources for each type

        Returns:
            True if request granted, False otherwise
        """
        pass  # TODO: Implement this

    def release_resources(self, process_id: int, release: List[int]) -> bool:
        """
        TODO: Release resources from a process.

        Steps:
        1. Check that release <= allocation[process_id]
        2. Update allocation and available
        3. Recalculate need

        Args:
            process_id: Process releasing resources
            release: Resources to release for each type

        Returns:
            True if successful, False otherwise
        """
        pass  # TODO: Implement this

    def is_safe_state(self) -> bool:
        """
        TODO: Implement the safety algorithm.

        Steps:
        1. Create work vector = available
        2. Create finish vector (all False)
        3. Find process i where finish[i] == False and need[i] <= work
        4. If found: work += allocation[i], finish[i] = True, repeat step 3
        5. If all finish[i] == True, state is safe

        Returns:
            True if state is safe, False otherwise
        """
        pass  # TODO: Implement this

    def _find_safe_sequence(self) -> Optional[List[int]]:
        """
        TODO: Find a safe sequence of process execution.

        This is similar to is_safe_state but returns the actual sequence.

        Returns:
            Safe sequence if one exists, None otherwise
        """
        pass  # TODO: Implement this

    def get_available(self) -> List[int]:
        """Get available resources."""
        return self.available.copy()

    def get_allocation(self, process_id: int) -> Optional[List[int]]:
        """Get allocation for a process."""
        if 0 <= process_id < self.num_processes:
            return self.allocation[process_id].copy()
        return None

    def get_need(self, process_id: int) -> Optional[List[int]]:
        """Get need for a process."""
        if 0 <= process_id < self.num_processes:
            return self.need[process_id].copy()
        return None

    def get_maximum(self, process_id: int) -> Optional[List[int]]:
        """Get maximum for a process."""
        if 0 <= process_id < self.num_processes:
            return self.maximum[process_id].copy()
        return None

    def _calculate_need(self) -> None:
        """
        TODO: Recalculate the need matrix.

        Need[i][j] = Maximum[i][j] - Allocation[i][j]
        """
        pass  # TODO: Implement this

    def deadlock_would_occur(self, process_id: int, request: List[int]) -> bool:
        """
        TODO: Check if granting this request would lead to deadlock.

        Simulate the allocation and check if resulting state is safe.

        Args:
            process_id: Process making the request
            request: Requested resources

        Returns:
            True if deadlock would occur, False otherwise
        """
        pass  # TODO: Implement this

    def total_resources_allocated(self) -> List[int]:
        """
        TODO: Calculate total resources currently allocated across all processes.

        Returns:
            List of total allocated resources for each type
        """
        pass  # TODO: Implement this


class TestBankerAlgorithm(unittest.TestCase):
    """Test cases for Banker's Algorithm."""

    def test_safe_state(self):
        """Test safe state detection."""
        # Classic example from textbooks
        available = [3, 3, 2]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

        banker = BankerAlgorithm(5, 3, available, maximum)

        self.assertTrue(banker.is_safe_state())

    def test_safe_request(self):
        """Test safe resource request."""
        available = [3, 3, 2]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

        banker = BankerAlgorithm(5, 3, available, maximum)

        # Process 1 requests (1, 0, 2)
        result = banker.request_resources(1, [1, 0, 2])
        self.assertTrue(result)

    def test_unsafe_request(self):
        """Test unsafe resource request."""
        available = [3, 3, 2]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

        banker = BankerAlgorithm(5, 3, available, maximum)

        # Request that would make state unsafe
        result = banker.request_resources(0, [4, 4, 3])
        self.assertFalse(result)

    def test_request_exceeds_need(self):
        """Test request exceeding need."""
        available = [3, 3, 2]
        maximum = [[2, 2, 2]]

        banker = BankerAlgorithm(1, 3, available, maximum)

        # Request more than maximum need
        result = banker.request_resources(0, [3, 3, 3])
        self.assertFalse(result)

    def test_request_exceeds_available(self):
        """Test request exceeding available resources."""
        available = [1, 1, 1]
        maximum = [[5, 5, 5]]

        banker = BankerAlgorithm(1, 3, available, maximum)

        # Request more than available
        result = banker.request_resources(0, [2, 2, 2])
        self.assertFalse(result)

    def test_release_resources(self):
        """Test releasing resources."""
        available = [3, 3, 2]
        maximum = [[5, 5, 5]]

        banker = BankerAlgorithm(1, 3, available, maximum)

        # Allocate some resources
        banker.request_resources(0, [2, 2, 1])

        before_available = banker.get_available()

        # Release resources
        banker.release_resources(0, [1, 1, 1])

        after_available = banker.get_available()

        self.assertEqual(after_available[0], before_available[0] + 1)
        self.assertEqual(after_available[1], before_available[1] + 1)
        self.assertEqual(after_available[2], before_available[2] + 1)

    def test_multiple_processes(self):
        """Test multiple processes requesting resources."""
        available = [10, 5, 7]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
        ]

        banker = BankerAlgorithm(3, 3, available, maximum)

        # Multiple processes request resources
        banker.request_resources(0, [0, 1, 0])
        banker.request_resources(1, [2, 0, 0])
        banker.request_resources(2, [3, 0, 2])

        self.assertTrue(banker.is_safe_state())

    def test_need_calculation(self):
        """Test need calculation."""
        available = [3, 3, 2]
        maximum = [[7, 5, 3]]

        banker = BankerAlgorithm(1, 3, available, maximum)

        banker.request_resources(0, [2, 2, 1])

        need = banker.get_need(0)

        self.assertEqual(need[0], 5)  # 7 - 2
        self.assertEqual(need[1], 3)  # 5 - 2
        self.assertEqual(need[2], 2)  # 3 - 1

    def test_deadlock_detection(self):
        """Test deadlock detection."""
        available = [2, 2, 2]
        maximum = [
            [5, 5, 5],
            [5, 5, 5],
        ]

        banker = BankerAlgorithm(2, 3, available, maximum)

        banker.request_resources(0, [2, 2, 2])

        # This request would likely cause deadlock
        self.assertTrue(banker.deadlock_would_occur(1, [2, 2, 2]))

    def test_total_resources(self):
        """Test total allocated resources calculation."""
        available = [3, 3, 2]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
        ]

        banker = BankerAlgorithm(2, 3, available, maximum)

        banker.request_resources(0, [1, 1, 1])
        banker.request_resources(1, [2, 1, 0])

        total = banker.total_resources_allocated()

        self.assertEqual(total[0], 3)  # 1 + 2
        self.assertEqual(total[1], 2)  # 1 + 1
        self.assertEqual(total[2], 1)  # 1 + 0

    def test_safe_sequence_exists(self):
        """Test finding safe sequence."""
        available = [3, 3, 2]
        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
        ]

        banker = BankerAlgorithm(3, 3, available, maximum)

        sequence = banker._find_safe_sequence()
        self.assertIsNotNone(sequence)

        if sequence:
            self.assertEqual(len(sequence), 3)

    def test_complete_workflow(self):
        """Test complete workflow."""
        available = [10, 10, 10]
        maximum = [
            [5, 5, 5],
            [4, 4, 4],
            [3, 3, 3],
        ]

        banker = BankerAlgorithm(3, 3, available, maximum)

        # Process 0 requests and gets resources
        banker.request_resources(0, [2, 2, 2])
        self.assertEqual(banker.get_allocation(0), [2, 2, 2])

        # Process 1 requests and gets resources
        banker.request_resources(1, [3, 3, 3])
        self.assertEqual(banker.get_allocation(1), [3, 3, 3])

        # Process 0 completes and releases
        banker.release_resources(0, [2, 2, 2])
        self.assertEqual(banker.get_allocation(0), [0, 0, 0])

        # More resources available now
        available = banker.get_available()
        self.assertEqual(available[0], 7)  # 10 - 3 (for process 1)


if __name__ == '__main__':
    unittest.main()
