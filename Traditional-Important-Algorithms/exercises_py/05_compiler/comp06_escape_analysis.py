# I AM NOT DONE

"""
comp06_escape_analysis.py

Escape analysis determines whether an object's lifetime is confined
to a specific scope. Non-escaping objects can be stack-allocated,
avoiding heap allocation overhead.

Your task: Implement a simple escape analysis for method calls.

An object escapes if:
- It is returned from a method
- It is stored in a field
- It is passed to another method

Otherwise, it can be stack-allocated.
"""

from typing import Dict, List, Optional, Set
from enum import Enum, auto
from dataclasses import dataclass
import unittest


class EscapeState(Enum):
    """Escape states for objects."""
    NO_ESCAPE = auto()       # Object doesn't escape - can be stack allocated
    ARG_ESCAPE = auto()      # Object escapes as method argument - may escape
    GLOBAL_ESCAPE = auto()   # Object escapes globally - definitely heap allocated


@dataclass
class ObjectId:
    """Represents an object identifier."""
    id: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, ObjectId) and self.id == other.id


class Instruction:
    """Base class for instructions."""
    pass


class New(Instruction):
    """Create a new object."""

    def __init__(self, obj_id: ObjectId):
        self.obj_id = obj_id

    def __repr__(self):
        return f"New({self.obj_id})"


class StoreField(Instruction):
    """Store object in a field: objects[target].field = source."""

    def __init__(self, target: ObjectId, field: str, source: ObjectId):
        self.target = target
        self.field = field
        self.source = source

    def __repr__(self):
        return f"StoreField({self.target}, {self.field}, {self.source})"


class LoadField(Instruction):
    """Load object from a field: dest = objects[source].field."""

    def __init__(self, dest: ObjectId, source: ObjectId, field: str):
        self.dest = dest
        self.source = source
        self.field = field

    def __repr__(self):
        return f"LoadField({self.dest}, {self.source}, {self.field})"


class Call(Instruction):
    """Call a method: result = method(args...)."""

    def __init__(self, result: Optional[ObjectId], method: str, args: List[ObjectId]):
        self.result = result
        self.method = method
        self.args = args

    def __repr__(self):
        return f"Call({self.result}, {self.method}, {self.args})"


class Return(Instruction):
    """Return an object from the method."""

    def __init__(self, obj_id: ObjectId):
        self.obj_id = obj_id

    def __repr__(self):
        return f"Return({self.obj_id})"


class EscapeAnalysis:
    """Performs escape analysis on a sequence of instructions."""

    def __init__(self, instructions: List[Instruction]):
        """Initialize with list of instructions."""
        self.instructions = instructions
        self.escape_states: Dict[ObjectId, EscapeState] = {}

    def analyze(self):
        """
        TODO: Analyze all instructions and determine escape state for each object.

        Start by marking all objects as NO_ESCAPE, then upgrade as needed.
        """
        pass  # TODO: Implement this

    def initialize_objects(self):
        """
        TODO: Find all New instructions and initialize their escape state to NO_ESCAPE.
        """
        pass  # TODO: Implement this

    def analyze_instruction(self, instr: Instruction):
        """
        TODO: Analyze a single instruction and update escape states.

        - StoreField: source escapes to at least ARG_ESCAPE
        - Call: arguments escape to at least ARG_ESCAPE
        - Return: returned object escapes to GLOBAL_ESCAPE
        """
        pass  # TODO: Implement this

    def mark_escape(self, obj: ObjectId, new_state: EscapeState):
        """
        TODO: Update escape state for an object.

        Only upgrade state (NO_ESCAPE -> ARG_ESCAPE -> GLOBAL_ESCAPE).
        Never downgrade.
        """
        pass  # TODO: Implement this

    def get_escape_state(self, obj: ObjectId) -> Optional[EscapeState]:
        """
        TODO: Return the escape state of an object.
        """
        pass  # TODO: Implement this

    def can_stack_allocate(self, obj: ObjectId) -> bool:
        """
        TODO: Return True if object can be stack allocated.

        Only NO_ESCAPE objects can be stack allocated.
        """
        pass  # TODO: Implement this

    def stack_allocatable_objects(self) -> List[ObjectId]:
        """
        TODO: Return all objects that can be stack allocated.
        """
        pass  # TODO: Implement this

    def escaping_objects(self) -> List[ObjectId]:
        """
        TODO: Return all objects that escape (ARG_ESCAPE or GLOBAL_ESCAPE).
        """
        pass  # TODO: Implement this

    def propagate_escape(self):
        """
        TODO: Propagate escape information through field stores.

        If an object A is stored in field of object B, and B escapes,
        then A must also escape at least as much as B.

        This requires multiple passes until fixpoint.
        """
        pass  # TODO: Implement this


# Unit Tests
class TestEscapeAnalysis(unittest.TestCase):

    def test_no_escape(self):
        # Object is created but never used
        instructions = [
            New(ObjectId(0)),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.NO_ESCAPE)
        self.assertTrue(analysis.can_stack_allocate(ObjectId(0)))

    def test_return_escape(self):
        # Object is returned - global escape
        instructions = [
            New(ObjectId(0)),
            Return(ObjectId(0)),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.GLOBAL_ESCAPE)
        self.assertFalse(analysis.can_stack_allocate(ObjectId(0)))

    def test_method_call_escape(self):
        # Object is passed to method - arg escape
        instructions = [
            New(ObjectId(0)),
            Call(None, "foo", [ObjectId(0)]),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.ARG_ESCAPE)
        self.assertFalse(analysis.can_stack_allocate(ObjectId(0)))

    def test_field_store_escape(self):
        # Object is stored in field - arg escape
        instructions = [
            New(ObjectId(0)),
            New(ObjectId(1)),
            StoreField(ObjectId(0), "f", ObjectId(1)),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        # Object 1 is stored in object 0's field, so it escapes
        self.assertEqual(analysis.get_escape_state(ObjectId(1)), EscapeState.ARG_ESCAPE)

    def test_multiple_objects(self):
        instructions = [
            New(ObjectId(0)),  # No escape
            New(ObjectId(1)),  # Returned
            New(ObjectId(2)),  # Used in call
            Return(ObjectId(1)),
            Call(None, "process", [ObjectId(2)]),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.NO_ESCAPE)
        self.assertEqual(analysis.get_escape_state(ObjectId(1)), EscapeState.GLOBAL_ESCAPE)
        self.assertEqual(analysis.get_escape_state(ObjectId(2)), EscapeState.ARG_ESCAPE)

        self.assertTrue(analysis.can_stack_allocate(ObjectId(0)))
        self.assertFalse(analysis.can_stack_allocate(ObjectId(1)))
        self.assertFalse(analysis.can_stack_allocate(ObjectId(2)))

    def test_transitive_escape(self):
        # Object 2 is stored in object 1, which is stored in object 0, which is returned
        # So all should eventually escape
        instructions = [
            New(ObjectId(0)),
            New(ObjectId(1)),
            New(ObjectId(2)),
            StoreField(ObjectId(1), "inner", ObjectId(2)),
            StoreField(ObjectId(0), "middle", ObjectId(1)),
            Return(ObjectId(0)),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()
        analysis.propagate_escape()  # Need to propagate through field stores

        # All objects should escape since obj0 is returned
        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.GLOBAL_ESCAPE)

        # Depending on implementation, these might be ARG_ESCAPE or GLOBAL_ESCAPE
        # At minimum they should not be NO_ESCAPE
        self.assertNotEqual(analysis.get_escape_state(ObjectId(1)), EscapeState.NO_ESCAPE)
        self.assertNotEqual(analysis.get_escape_state(ObjectId(2)), EscapeState.NO_ESCAPE)

    def test_local_use_only(self):
        # Object is created, has field accessed, but never escapes
        instructions = [
            New(ObjectId(0)),
            New(ObjectId(1)),
            LoadField(ObjectId(1), ObjectId(0), "value"),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        # LoadField doesn't cause escape - just reading
        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.NO_ESCAPE)

    def test_call_result(self):
        # Result from method call doesn't escape
        instructions = [
            Call(ObjectId(0), "create", []),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        # Object returned from call starts as NO_ESCAPE in this context
        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.NO_ESCAPE)

    def test_multiple_calls(self):
        instructions = [
            New(ObjectId(0)),
            Call(None, "process", [ObjectId(0)]),
            Call(None, "finalize", [ObjectId(0)]),
        ]

        analysis = EscapeAnalysis(instructions)
        analysis.analyze()

        # Passed to multiple methods - still ARG_ESCAPE
        self.assertEqual(analysis.get_escape_state(ObjectId(0)), EscapeState.ARG_ESCAPE)


if __name__ == '__main__':
    unittest.main()
