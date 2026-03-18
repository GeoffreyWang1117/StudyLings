# I AM NOT DONE

"""
Exercise: Escape Analysis

Escape analysis determines whether an object's lifetime is confined
to a specific scope. Non-escaping objects can be stack-allocated,
avoiding GC overhead.

Your task: Implement a simple escape analysis for a toy language.
"""

from enum import Enum


class EscapeStatus(Enum):
    """Escape status of a variable"""
    NO_ESCAPE = "NoEscape"          # Object doesn't escape
    ARG_ESCAPE = "ArgEscape"        # Escapes as function argument
    GLOBAL_ESCAPE = "GlobalEscape"  # Escapes to global scope


class Expr:
    """Base class for expressions"""
    pass


class Alloc(Expr):
    """Allocate new object"""
    pass


class Var(Expr):
    """Variable reference"""

    def __init__(self, var_id):
        self.var_id = var_id


class Assign(Expr):
    """Assignment: var = expr"""

    def __init__(self, var_id, expr):
        self.var_id = var_id
        self.expr = expr


class Return(Expr):
    """Return statement"""

    def __init__(self, var_id):
        self.var_id = var_id


class Call(Expr):
    """Function call"""

    def __init__(self, func_id, args):
        self.func_id = func_id
        self.args = args  # List of var_ids


class Field(Expr):
    """Field access: obj.field"""

    def __init__(self, var_id, field_name):
        self.var_id = var_id
        self.field_name = field_name


class StoreField(Expr):
    """Field store: obj.field = value"""

    def __init__(self, obj_id, field_name, value_id):
        self.obj_id = obj_id
        self.field_name = field_name
        self.value_id = value_id


class EscapeAnalyzer:
    """Escape analyzer for variables"""

    def __init__(self, expressions):
        self.expressions = expressions
        self.var_status = {}  # var_id -> EscapeStatus

    def analyze(self):
        """Perform escape analysis on all expressions"""
        # TODO: Perform escape analysis on all expressions
        # Update var_status for each variable
        pass

    def _analyze_expr(self, expr):
        """Analyze a single expression"""
        # TODO: Analyze a single expression
        # Update escape status based on how variables are used
        pass

    def _mark_escape(self, var_id, status):
        """Mark a variable as escaping"""
        # TODO: Mark a variable as escaping
        # If already marked with "worse" escape status, keep it
        # Order: NoEscape < ArgEscape < GlobalEscape
        pass

    def get_status(self, var_id):
        """Get escape status of a variable"""
        return self.var_status.get(var_id)

    def can_stack_allocate(self, var_id):
        """Return true if variable can be stack allocated"""
        # TODO: Return true if variable can be stack allocated
        # Only NoEscape variables can be stack allocated
        pass

    def escaping_vars(self):
        """Return all variables that escape"""
        # TODO: Return all variables that escape (ArgEscape or GlobalEscape)
        pass


import unittest


class TestEscapeAnalysis(unittest.TestCase):
    def test_no_escape(self):
        exprs = [
            Assign(0, Alloc()),
            # x = new Object(); x doesn't escape
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertEqual(analyzer.get_status(0), EscapeStatus.NO_ESCAPE)
        self.assertTrue(analyzer.can_stack_allocate(0))

    def test_return_escape(self):
        exprs = [
            Assign(0, Alloc()),
            Return(0),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertEqual(analyzer.get_status(0), EscapeStatus.GLOBAL_ESCAPE)
        self.assertFalse(analyzer.can_stack_allocate(0))

    def test_arg_escape(self):
        exprs = [
            Assign(0, Alloc()),
            Call(1, [0]),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertEqual(analyzer.get_status(0), EscapeStatus.ARG_ESCAPE)
        self.assertFalse(analyzer.can_stack_allocate(0))

    def test_field_store_escape(self):
        exprs = [
            Assign(0, Alloc()),
            Assign(1, Alloc()),
            StoreField(0, "field", 1),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        # var 1 escapes because it's stored in a field
        self.assertEqual(analyzer.get_status(1), EscapeStatus.ARG_ESCAPE)

    def test_multiple_vars(self):
        exprs = [
            Assign(0, Alloc()),  # no escape
            Assign(1, Alloc()),  # returns
            Assign(2, Alloc()),  # arg escape
            Return(1),
            Call(3, [2]),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertTrue(analyzer.can_stack_allocate(0))
        self.assertFalse(analyzer.can_stack_allocate(1))
        self.assertFalse(analyzer.can_stack_allocate(2))

    def test_escaping_vars_list(self):
        exprs = [
            Assign(0, Alloc()),
            Assign(1, Alloc()),
            Assign(2, Alloc()),
            Return(1),
            Call(3, [2]),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        escaping = analyzer.escaping_vars()
        self.assertIn(1, escaping)
        self.assertIn(2, escaping)
        self.assertNotIn(0, escaping)

    def test_no_allocation(self):
        exprs = []

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertEqual(len(analyzer.escaping_vars()), 0)

    def test_worst_status_wins(self):
        exprs = [
            Assign(0, Alloc()),
            Call(1, [0]),      # ArgEscape
            Return(0),         # GlobalEscape
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        # Should be GlobalEscape (worse than ArgEscape)
        self.assertEqual(analyzer.get_status(0), EscapeStatus.GLOBAL_ESCAPE)

    def test_field_access_no_escape(self):
        exprs = [
            Assign(0, Alloc()),
            Field(0, "field"),  # Just reading field doesn't cause escape
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        # Reading field doesn't cause escape
        self.assertEqual(analyzer.get_status(0), EscapeStatus.NO_ESCAPE)

    def test_multiple_calls(self):
        exprs = [
            Assign(0, Alloc()),
            Call(1, [0]),
            Call(2, [0]),
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        self.assertEqual(analyzer.get_status(0), EscapeStatus.ARG_ESCAPE)

    def test_transitive_escape(self):
        exprs = [
            Assign(0, Alloc()),
            Assign(1, Alloc()),
            StoreField(0, "field", 1),  # 1 stored in 0
            Return(0),                   # 0 escapes
        ]

        analyzer = EscapeAnalyzer(exprs)
        analyzer.analyze()

        # Both should escape
        self.assertEqual(analyzer.get_status(0), EscapeStatus.GLOBAL_ESCAPE)
        # 1 at least has ArgEscape from field store
        self.assertIn(analyzer.get_status(1), [EscapeStatus.ARG_ESCAPE, EscapeStatus.GLOBAL_ESCAPE])


if __name__ == '__main__':
    unittest.main()
