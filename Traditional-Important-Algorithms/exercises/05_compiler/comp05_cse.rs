// comp05_cse.rs
//
// Common Subexpression Elimination (CSE) is an optimization that identifies
// expressions that are computed multiple times with the same operands and
// replaces them with a single computation stored in a temporary variable.
//
// Your task: Implement CSE for a simple expression language.
//
// Example transformation:
//   a = b + c
//   d = b + c    →   a = b + c
//   e = a * d        d = a
//                    e = a * a

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Expr {
    Var(String),
    Const(i64),
    Binary {
        op: BinaryOp,
        left: Box<Expr>,
        right: Box<Expr>,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Statement {
    pub target: String,
    pub expr: Expr,
}

impl Statement {
    pub fn new(target: String, expr: Expr) -> Self {
        Self { target, expr }
    }
}

pub struct CSE {
    // Maps canonical expression to the variable that holds its value
    expr_to_var: HashMap<Expr, String>,
    // Counter for generating temporary variables
    temp_counter: usize,
}

impl CSE {
    pub fn new() -> Self {
        Self {
            expr_to_var: HashMap::new(),
            temp_counter: 0,
        }
    }

    pub fn optimize(&mut self, statements: Vec<Statement>) -> Vec<Statement> {
        // TODO: Optimize a sequence of statements
        // Process each statement, identifying and eliminating common subexpressions
        // Return the optimized sequence
        todo!()
    }

    fn optimize_statement(&mut self, stmt: Statement) -> Vec<Statement> {
        // TODO: Optimize a single statement
        // 1. Recursively process the expression to find common subexpressions
        // 2. Replace common subexpressions with variables
        // 3. May generate multiple statements (for extracted subexpressions)
        todo!()
    }

    fn process_expr(&mut self, expr: Expr) -> (Expr, Vec<Statement>) {
        // TODO: Process an expression to extract common subexpressions
        // Returns: (simplified_expr, new_statements_for_temps)
        //
        // Algorithm:
        // 1. For constants and variables, return as-is
        // 2. For binary expressions:
        //    a. Recursively process left and right operands
        //    b. Create canonical form of the expression
        //    c. Check if we've seen this expression before
        //    d. If yes, return the variable that holds it
        //    e. If no, record it and return the expression
        todo!()
    }

    fn canonicalize(&self, expr: &Expr) -> Expr {
        // TODO: Convert expression to canonical form for comparison
        // For commutative operations (Add, Mul), order operands consistently
        // This allows "a + b" to match "b + a"
        todo!()
    }

    fn is_commutative(op: BinaryOp) -> bool {
        // Helper: check if operation is commutative
        matches!(op, BinaryOp::Add | BinaryOp::Mul)
    }

    fn generate_temp(&mut self) -> String {
        // Helper: generate a unique temporary variable name
        let name = format!("_t{}", self.temp_counter);
        self.temp_counter += 1;
        name
    }

    pub fn reset(&mut self) {
        // TODO: Reset the CSE state for a new basic block
        // Clear the expression-to-variable mapping
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn var(s: &str) -> Expr {
        Expr::Var(s.to_string())
    }

    fn const_(n: i64) -> Expr {
        Expr::Const(n)
    }

    fn binary(op: BinaryOp, left: Expr, right: Expr) -> Expr {
        Expr::Binary {
            op,
            left: Box::new(left),
            right: Box::new(right),
        }
    }

    fn stmt(target: &str, expr: Expr) -> Statement {
        Statement::new(target.to_string(), expr)
    }

    #[test]
    fn test_simple_cse() {
        let mut cse = CSE::new();

        // a = b + c
        // d = b + c
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("b"), var("c"))),
            stmt("d", binary(BinaryOp::Add, var("b"), var("c"))),
        ];

        let optimized = cse.optimize(statements);

        // Second statement should reuse first
        assert_eq!(optimized.len(), 2);
        assert_eq!(optimized[1].expr, var("a"));
    }

    #[test]
    fn test_no_common_subexpr() {
        let mut cse = CSE::new();

        // a = b + c
        // d = e + f
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("b"), var("c"))),
            stmt("d", binary(BinaryOp::Add, var("e"), var("f"))),
        ];

        let optimized = cse.optimize(statements);

        // No changes expected
        assert_eq!(optimized.len(), 2);
        assert_eq!(optimized[0].expr, binary(BinaryOp::Add, var("b"), var("c")));
        assert_eq!(optimized[1].expr, binary(BinaryOp::Add, var("e"), var("f")));
    }

    #[test]
    fn test_commutative_matching() {
        let mut cse = CSE::new();

        // a = b + c
        // d = c + b  (should match a = b + c)
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("b"), var("c"))),
            stmt("d", binary(BinaryOp::Add, var("c"), var("b"))),
        ];

        let optimized = cse.optimize(statements);

        // Second should reuse first
        assert_eq!(optimized.len(), 2);
        assert_eq!(optimized[1].expr, var("a"));
    }

    #[test]
    fn test_non_commutative() {
        let mut cse = CSE::new();

        // a = b - c
        // d = c - b  (should NOT match)
        let statements = vec![
            stmt("a", binary(BinaryOp::Sub, var("b"), var("c"))),
            stmt("d", binary(BinaryOp::Sub, var("c"), var("b"))),
        ];

        let optimized = cse.optimize(statements);

        // No changes - subtraction is not commutative
        assert_eq!(optimized.len(), 2);
        assert_eq!(optimized[1].expr, binary(BinaryOp::Sub, var("c"), var("b")));
    }

    #[test]
    fn test_nested_expressions() {
        let mut cse = CSE::new();

        // a = b + c
        // d = (b + c) * e
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("b"), var("c"))),
            stmt("d", binary(
                BinaryOp::Mul,
                binary(BinaryOp::Add, var("b"), var("c")),
                var("e"),
            )),
        ];

        let optimized = cse.optimize(statements);

        // The nested b + c should be replaced with 'a'
        assert_eq!(optimized[1].expr, binary(BinaryOp::Mul, var("a"), var("e")));
    }

    #[test]
    fn test_multiple_uses() {
        let mut cse = CSE::new();

        // a = x + y
        // b = x + y
        // c = x + y
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("x"), var("y"))),
            stmt("b", binary(BinaryOp::Add, var("x"), var("y"))),
            stmt("c", binary(BinaryOp::Add, var("x"), var("y"))),
        ];

        let optimized = cse.optimize(statements);

        // All should refer to first computation
        assert_eq!(optimized.len(), 3);
        assert_eq!(optimized[1].expr, var("a"));
        assert_eq!(optimized[2].expr, var("a"));
    }

    #[test]
    fn test_complex_expression() {
        let mut cse = CSE::new();

        // a = (b + c) * (d + e)
        // f = (b + c) * 2
        // g = (d + e) + 10
        let statements = vec![
            stmt("a", binary(
                BinaryOp::Mul,
                binary(BinaryOp::Add, var("b"), var("c")),
                binary(BinaryOp::Add, var("d"), var("e")),
            )),
            stmt("f", binary(
                BinaryOp::Mul,
                binary(BinaryOp::Add, var("b"), var("c")),
                const_(2),
            )),
            stmt("g", binary(
                BinaryOp::Add,
                binary(BinaryOp::Add, var("d"), var("e")),
                const_(10),
            )),
        ];

        let optimized = cse.optimize(statements);

        // Should extract (b + c) and (d + e) as common subexpressions
        // The exact number of statements depends on implementation,
        // but there should be some optimization
        assert!(optimized.len() >= 3);
    }

    #[test]
    fn test_constants() {
        let mut cse = CSE::new();

        // a = 5 + 10
        // b = 5 + 10
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, const_(5), const_(10))),
            stmt("b", binary(BinaryOp::Add, const_(5), const_(10))),
        ];

        let optimized = cse.optimize(statements);

        // Constants should be matched
        assert_eq!(optimized.len(), 2);
        assert_eq!(optimized[1].expr, var("a"));
    }

    #[test]
    fn test_chained_dependencies() {
        let mut cse = CSE::new();

        // a = b + c
        // d = a + e
        // f = b + c
        let statements = vec![
            stmt("a", binary(BinaryOp::Add, var("b"), var("c"))),
            stmt("d", binary(BinaryOp::Add, var("a"), var("e"))),
            stmt("f", binary(BinaryOp::Add, var("b"), var("c"))),
        ];

        let optimized = cse.optimize(statements);

        // 'f' should reuse 'a'
        assert_eq!(optimized.len(), 3);
        assert_eq!(optimized[2].expr, var("a"));
    }
}
