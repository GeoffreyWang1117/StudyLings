# I AM NOT DONE

"""
comp05_cse.py

Common Subexpression Elimination (CSE) is an optimization that identifies
expressions that are computed multiple times with the same operands and
replaces them with a single computation stored in a temporary variable.

Your task: Implement CSE for a simple expression language.

Example transformation:
  a = b + c
  d = b + c    →   a = b + c
  e = a * d        d = a
                   e = a * a
"""

from typing import Dict, List, Tuple
from enum import Enum, auto
import unittest


class BinaryOp(Enum):
    """Binary operators."""
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


class Expr:
    """Base class for expressions."""
    pass


class Var(Expr):
    """Variable reference."""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(("Var", self.name))

    def __repr__(self):
        return f"Var({self.name})"


class Const(Expr):
    """Constant value."""

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Const) and self.value == other.value

    def __hash__(self):
        return hash(("Const", self.value))

    def __repr__(self):
        return f"Const({self.value})"


class Binary(Expr):
    """Binary expression."""

    def __init__(self, op: BinaryOp, left: Expr, right: Expr):
        self.op = op
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Binary) and
                self.op == other.op and
                self.left == other.left and
                self.right == other.right)

    def __hash__(self):
        return hash(("Binary", self.op, self.left, self.right))

    def __repr__(self):
        return f"Binary({self.op}, {self.left}, {self.right})"


class Statement:
    """Assignment statement."""

    def __init__(self, target: str, expr: Expr):
        self.target = target
        self.expr = expr

    def __eq__(self, other):
        return (isinstance(other, Statement) and
                self.target == other.target and
                self.expr == other.expr)

    def __repr__(self):
        return f"Statement({self.target}, {self.expr})"


class CSE:
    """Common Subexpression Elimination optimizer."""

    def __init__(self):
        """Initialize CSE optimizer."""
        # Maps canonical expression to the variable that holds its value
        self.expr_to_var: Dict[Expr, str] = {}
        # Counter for generating temporary variables
        self.temp_counter = 0

    def optimize(self, statements: List[Statement]) -> List[Statement]:
        """
        TODO: Optimize a sequence of statements.

        Process each statement, identifying and eliminating common subexpressions.
        Return the optimized sequence.
        """
        pass  # TODO: Implement this

    def optimize_statement(self, stmt: Statement) -> List[Statement]:
        """
        TODO: Optimize a single statement.

        1. Recursively process the expression to find common subexpressions
        2. Replace common subexpressions with variables
        3. May generate multiple statements (for extracted subexpressions)

        Return a list of statements (might be more than one)
        """
        pass  # TODO: Implement this

    def process_expr(self, expr: Expr) -> Tuple[Expr, List[Statement]]:
        """
        TODO: Process an expression to extract common subexpressions.

        Returns: (simplified_expr, new_statements_for_temps)

        Algorithm:
        1. For constants and variables, return as-is
        2. For binary expressions:
           a. Recursively process left and right operands
           b. Create canonical form of the expression
           c. Check if we've seen this expression before
           d. If yes, return the variable that holds it
           e. If no, record it and return the expression
        """
        pass  # TODO: Implement this

    def canonicalize(self, expr: Expr) -> Expr:
        """
        TODO: Convert expression to canonical form for comparison.

        For commutative operations (ADD, MUL), order operands consistently.
        This allows "a + b" to match "b + a".
        Compare operands by their hash or representation, and swap if needed.
        """
        pass  # TODO: Implement this

    @staticmethod
    def is_commutative(op: BinaryOp) -> bool:
        """Check if operation is commutative."""
        return op in (BinaryOp.ADD, BinaryOp.MUL)

    def generate_temp(self) -> str:
        """Generate a unique temporary variable name."""
        name = f"_t{self.temp_counter}"
        self.temp_counter += 1
        return name

    def reset(self):
        """
        TODO: Reset the CSE state for a new basic block.

        Clear the expression-to-variable mapping.
        """
        pass  # TODO: Implement this


# Unit Tests
class TestCSE(unittest.TestCase):

    def test_simple_cse(self):
        cse = CSE()

        # a = b + c
        # d = b + c
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
        ]

        optimized = cse.optimize(statements)

        # Second statement should reuse first
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[1].expr, Var("a"))

    def test_no_common_subexpr(self):
        cse = CSE()

        # a = b + c
        # d = e + f
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.ADD, Var("e"), Var("f"))),
        ]

        optimized = cse.optimize(statements)

        # No changes expected
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[0].expr, Binary(BinaryOp.ADD, Var("b"), Var("c")))
        self.assertEqual(optimized[1].expr, Binary(BinaryOp.ADD, Var("e"), Var("f")))

    def test_commutative_matching(self):
        cse = CSE()

        # a = b + c
        # d = c + b  (should match a = b + c)
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.ADD, Var("c"), Var("b"))),
        ]

        optimized = cse.optimize(statements)

        # Second should reuse first
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[1].expr, Var("a"))

    def test_non_commutative(self):
        cse = CSE()

        # a = b - c
        # d = c - b  (should NOT match)
        statements = [
            Statement("a", Binary(BinaryOp.SUB, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.SUB, Var("c"), Var("b"))),
        ]

        optimized = cse.optimize(statements)

        # No changes - subtraction is not commutative
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[1].expr, Binary(BinaryOp.SUB, Var("c"), Var("b")))

    def test_nested_expressions(self):
        cse = CSE()

        # a = b + c
        # d = (b + c) * e
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.MUL,
                                 Binary(BinaryOp.ADD, Var("b"), Var("c")),
                                 Var("e"))),
        ]

        optimized = cse.optimize(statements)

        # The nested b + c should be replaced with 'a'
        self.assertEqual(optimized[1].expr, Binary(BinaryOp.MUL, Var("a"), Var("e")))

    def test_multiple_uses(self):
        cse = CSE()

        # a = x + y
        # b = x + y
        # c = x + y
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("x"), Var("y"))),
            Statement("b", Binary(BinaryOp.ADD, Var("x"), Var("y"))),
            Statement("c", Binary(BinaryOp.ADD, Var("x"), Var("y"))),
        ]

        optimized = cse.optimize(statements)

        # All should refer to first computation
        self.assertEqual(len(optimized), 3)
        self.assertEqual(optimized[1].expr, Var("a"))
        self.assertEqual(optimized[2].expr, Var("a"))

    def test_complex_expression(self):
        cse = CSE()

        # a = (b + c) * (d + e)
        # f = (b + c) * 2
        # g = (d + e) + 10
        statements = [
            Statement("a", Binary(BinaryOp.MUL,
                                 Binary(BinaryOp.ADD, Var("b"), Var("c")),
                                 Binary(BinaryOp.ADD, Var("d"), Var("e")))),
            Statement("f", Binary(BinaryOp.MUL,
                                 Binary(BinaryOp.ADD, Var("b"), Var("c")),
                                 Const(2))),
            Statement("g", Binary(BinaryOp.ADD,
                                 Binary(BinaryOp.ADD, Var("d"), Var("e")),
                                 Const(10))),
        ]

        optimized = cse.optimize(statements)

        # Should extract (b + c) and (d + e) as common subexpressions
        # The exact number of statements depends on implementation,
        # but there should be some optimization
        self.assertTrue(len(optimized) >= 3)

    def test_constants(self):
        cse = CSE()

        # a = 5 + 10
        # b = 5 + 10
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Const(5), Const(10))),
            Statement("b", Binary(BinaryOp.ADD, Const(5), Const(10))),
        ]

        optimized = cse.optimize(statements)

        # Constants should be matched
        self.assertEqual(len(optimized), 2)
        self.assertEqual(optimized[1].expr, Var("a"))

    def test_chained_dependencies(self):
        cse = CSE()

        # a = b + c
        # d = a + e
        # f = b + c
        statements = [
            Statement("a", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
            Statement("d", Binary(BinaryOp.ADD, Var("a"), Var("e"))),
            Statement("f", Binary(BinaryOp.ADD, Var("b"), Var("c"))),
        ]

        optimized = cse.optimize(statements)

        # 'f' should reuse 'a'
        self.assertEqual(len(optimized), 3)
        self.assertEqual(optimized[2].expr, Var("a"))


if __name__ == '__main__':
    unittest.main()
