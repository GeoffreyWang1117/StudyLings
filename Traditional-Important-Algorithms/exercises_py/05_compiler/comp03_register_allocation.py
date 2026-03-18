# I AM NOT DONE

"""
comp03_register_allocation.py

Register allocation assigns virtual registers (unlimited) to physical
registers (limited) using graph coloring. Variables that are live at
the same time cannot share the same register - they interfere.

Your task: Implement register allocation using graph coloring.

Algorithm:
1. Build an interference graph where nodes are variables
2. Nodes are connected if variables are live simultaneously
3. Color the graph with K colors (K = number of physical registers)
4. If successful, each color represents a physical register
"""

from typing import Dict, Set, List, Optional
import unittest


class VarId:
    """Represents a variable identifier."""

    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, VarId) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"VarId({self.id})"


class RegisterId:
    """Represents a physical register identifier."""

    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, RegisterId) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"RegisterId({self.id})"


class InterferenceGraph:
    """Represents an interference graph for register allocation."""

    def __init__(self):
        """Initialize an empty interference graph."""
        # Adjacency list representation: var_id -> set of interfering var_ids
        self.edges: Dict[VarId, Set[VarId]] = {}

    def add_variable(self, var: VarId):
        """
        TODO: Add a variable to the graph (with no edges initially).

        If the variable already exists, do nothing.
        """
        pass  # TODO: Implement this

    def add_interference(self, var1: VarId, var2: VarId):
        """
        TODO: Add an edge between two variables (undirected).

        This means they interfere and cannot share a register.
        Make sure both variables exist in the graph first.
        Add var2 to var1's neighbors and var1 to var2's neighbors.
        """
        pass  # TODO: Implement this

    def neighbors(self, var: VarId) -> List[VarId]:
        """
        TODO: Return all neighbors (interfering variables) of var.

        Return as a list (can be in any order).
        Return empty list if variable not in graph.
        """
        pass  # TODO: Implement this

    def degree(self, var: VarId) -> int:
        """
        TODO: Return the degree (number of neighbors) of var.

        Return 0 if variable not in graph.
        """
        pass  # TODO: Implement this

    def remove_variable(self, var: VarId):
        """
        TODO: Remove a variable and all its edges from the graph.

        1. Remove var from all of its neighbors' neighbor sets
        2. Remove var from the edges dictionary
        """
        pass  # TODO: Implement this

    def variables(self) -> List[VarId]:
        """
        TODO: Return all variables in the graph.

        Return as a list (can be in any order).
        """
        pass  # TODO: Implement this


class RegisterAllocator:
    """Performs register allocation using graph coloring."""

    def __init__(self, graph: InterferenceGraph, num_registers: int):
        """Initialize allocator with interference graph and number of registers."""
        self.graph = graph
        self.num_registers = num_registers

    def allocate(self) -> tuple[Dict[VarId, RegisterId], List[VarId]]:
        """
        TODO: Allocate registers using graph coloring.

        Return (mapping, spilled_vars) where:
        - mapping: dict from VarId to RegisterId if successful
        - spilled_vars: list of variables that couldn't be allocated

        Algorithm:
        1. Build a stack by repeatedly removing nodes with degree < num_registers
        2. If all remaining nodes have degree >= num_registers, pick one to spill
        3. Color nodes by popping from stack and assigning colors
        4. A node can use any color not used by its neighbors
        5. If a node can't be colored, add it to spill list

        Return ({mapping}, []) on success or ({partial_mapping}, [spilled_vars]) on failure
        """
        pass  # TODO: Implement this

    def simplify(self, stack: List[VarId]) -> Optional[VarId]:
        """
        TODO: Find a variable with degree < num_registers.

        Remove it from graph and push onto stack.
        Return the variable if found, None if all variables have high degree.
        """
        pass  # TODO: Implement this

    def color_graph(self, stack: List[VarId]) -> tuple[Dict[VarId, RegisterId], List[VarId]]:
        """
        TODO: Color the graph by processing variables in reverse stack order.

        For each variable, assign it a color not used by its neighbors.
        If no color available, add to spill list.

        Return (mapping, spilled_vars)
        """
        pass  # TODO: Implement this

    def find_available_register(self, var: VarId, coloring: Dict[VarId, RegisterId]) -> Optional[RegisterId]:
        """
        TODO: Find a register not used by any neighbor of var.

        1. Get all neighbors of var
        2. Collect their assigned registers from coloring
        3. Find the first register (0 to num_registers-1) not in that set
        4. Return RegisterId or None if all registers are taken
        """
        pass  # TODO: Implement this


# Unit Tests
class TestRegisterAllocation(unittest.TestCase):

    def test_interference_graph(self):
        graph = InterferenceGraph()

        graph.add_variable(VarId(0))
        graph.add_variable(VarId(1))
        graph.add_variable(VarId(2))

        graph.add_interference(VarId(0), VarId(1))
        graph.add_interference(VarId(1), VarId(2))

        self.assertEqual(graph.degree(VarId(0)), 1)
        self.assertEqual(graph.degree(VarId(1)), 2)
        self.assertEqual(graph.degree(VarId(2)), 1)

        self.assertEqual(graph.neighbors(VarId(0)), [VarId(1)])

    def test_simple_allocation(self):
        # Three variables, no interference, should all get different registers
        graph = InterferenceGraph()
        graph.add_variable(VarId(0))
        graph.add_variable(VarId(1))
        graph.add_variable(VarId(2))

        allocator = RegisterAllocator(graph, 3)
        mapping, spilled = allocator.allocate()

        self.assertEqual(len(spilled), 0)
        self.assertEqual(len(mapping), 3)

    def test_linear_interference(self):
        # Variables: 0 - 1 - 2 (chain)
        # Can be colored with 2 registers
        graph = InterferenceGraph()
        graph.add_variable(VarId(0))
        graph.add_variable(VarId(1))
        graph.add_variable(VarId(2))

        graph.add_interference(VarId(0), VarId(1))
        graph.add_interference(VarId(1), VarId(2))

        allocator = RegisterAllocator(graph, 2)
        mapping, spilled = allocator.allocate()

        self.assertEqual(len(spilled), 0)

        # var0 and var2 should get same register (no interference)
        # var1 should get different register
        self.assertEqual(mapping[VarId(0)], mapping[VarId(2)])
        self.assertNotEqual(mapping[VarId(0)], mapping[VarId(1)])

    def test_triangle_interference(self):
        # Variables: 0 - 1 - 2 - 0 (triangle)
        # Needs 3 registers minimum
        graph = InterferenceGraph()
        graph.add_variable(VarId(0))
        graph.add_variable(VarId(1))
        graph.add_variable(VarId(2))

        graph.add_interference(VarId(0), VarId(1))
        graph.add_interference(VarId(1), VarId(2))
        graph.add_interference(VarId(2), VarId(0))

        # With 3 registers, should succeed
        allocator = RegisterAllocator(InterferenceGraph(), 3)
        # Rebuild graph
        allocator.graph.add_variable(VarId(0))
        allocator.graph.add_variable(VarId(1))
        allocator.graph.add_variable(VarId(2))
        allocator.graph.add_interference(VarId(0), VarId(1))
        allocator.graph.add_interference(VarId(1), VarId(2))
        allocator.graph.add_interference(VarId(2), VarId(0))

        mapping, spilled = allocator.allocate()
        self.assertEqual(len(spilled), 0)

        # With 2 registers, should fail (need to spill)
        graph2 = InterferenceGraph()
        graph2.add_variable(VarId(0))
        graph2.add_variable(VarId(1))
        graph2.add_variable(VarId(2))
        graph2.add_interference(VarId(0), VarId(1))
        graph2.add_interference(VarId(1), VarId(2))
        graph2.add_interference(VarId(2), VarId(0))

        allocator2 = RegisterAllocator(graph2, 2)
        mapping2, spilled2 = allocator2.allocate()
        self.assertTrue(len(spilled2) > 0)

    def test_complex_graph(self):
        # More complex interference pattern
        graph = InterferenceGraph()
        for i in range(5):
            graph.add_variable(VarId(i))

        # Create a more complex pattern
        graph.add_interference(VarId(0), VarId(1))
        graph.add_interference(VarId(0), VarId(2))
        graph.add_interference(VarId(1), VarId(2))
        graph.add_interference(VarId(2), VarId(3))
        graph.add_interference(VarId(3), VarId(4))

        allocator = RegisterAllocator(graph, 3)
        mapping, spilled = allocator.allocate()

        self.assertEqual(len(spilled), 0)

        # Verify no interfering variables share a register
        self.assertNotEqual(mapping[VarId(0)], mapping[VarId(1)])
        self.assertNotEqual(mapping[VarId(0)], mapping[VarId(2)])
        self.assertNotEqual(mapping[VarId(1)], mapping[VarId(2)])
        self.assertNotEqual(mapping[VarId(2)], mapping[VarId(3)])
        self.assertNotEqual(mapping[VarId(3)], mapping[VarId(4)])

    def test_spilling(self):
        # Complete graph K4 needs 4 colors
        graph = InterferenceGraph()
        for i in range(4):
            graph.add_variable(VarId(i))

        for i in range(4):
            for j in range(i + 1, 4):
                graph.add_interference(VarId(i), VarId(j))

        # With 3 registers, must spill at least one variable
        allocator = RegisterAllocator(graph, 3)
        mapping, spilled = allocator.allocate()

        self.assertTrue(len(spilled) > 0)


if __name__ == '__main__':
    unittest.main()
