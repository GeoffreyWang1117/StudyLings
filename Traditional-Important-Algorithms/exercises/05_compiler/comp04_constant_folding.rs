// comp04_constant_folding.rs
//
// Constant folding is a compiler optimization that evaluates constant
// expressions at compile time rather than runtime. For example, "2 + 3"
// can be replaced with "5" before the program runs.
//
// Your task: Implement constant folding for a simple expression language.
//
// Optimizations to implement:
// - Arithmetic: 2 + 3 → 5, 10 * 0 → 0
// - Boolean: true && false → false, !true → false
// - Algebraic identities: x + 0 → x, x * 1 → x, x * 0 → 0

// I AM NOT DONE

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Int(i64),
    Bool(bool),
    Var(String),
    Binary {
        op: BinaryOp,
        left: Box<Expr>,
        right: Box<Expr>,
    },
    Unary {
        op: UnaryOp,
        operand: Box<Expr>,
    },
    If {
        condition: Box<Expr>,
        then_branch: Box<Expr>,
        else_branch: Box<Expr>,
    },
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
    Eq,
    Lt,
    And,
    Or,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum UnaryOp {
    Neg,
    Not,
}

impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Expr::Int(n) => write!(f, "{}", n),
            Expr::Bool(b) => write!(f, "{}", b),
            Expr::Var(s) => write!(f, "{}", s),
            Expr::Binary { op, left, right } => {
                write!(f, "({} {:?} {})", left, op, right)
            }
            Expr::Unary { op, operand } => {
                write!(f, "({:?} {})", op, operand)
            }
            Expr::If { condition, then_branch, else_branch } => {
                write!(f, "(if {} then {} else {})", condition, then_branch, else_branch)
            }
        }
    }
}

pub struct ConstantFolder;

impl ConstantFolder {
    pub fn new() -> Self {
        Self
    }

    pub fn fold(&self, expr: Expr) -> Expr {
        // TODO: Recursively fold constants in the expression
        // Process children first (bottom-up), then try to fold this node
        todo!()
    }

    fn fold_binary(&self, op: BinaryOp, left: Expr, right: Expr) -> Expr {
        // TODO: Fold binary operations
        // First, recursively fold left and right
        // Then, if both are constants, evaluate
        // Also apply algebraic identities (x + 0, x * 1, x * 0, etc.)
        todo!()
    }

    fn fold_unary(&self, op: UnaryOp, operand: Expr) -> Expr {
        // TODO: Fold unary operations
        // First, recursively fold operand
        // Then, if operand is constant, evaluate
        todo!()
    }

    fn fold_if(&self, condition: Expr, then_branch: Expr, else_branch: Expr) -> Expr {
        // TODO: Fold if expressions
        // First, recursively fold all branches
        // If condition is constant, return the appropriate branch
        todo!()
    }

    fn eval_binary_int(&self, op: BinaryOp, left: i64, right: i64) -> Option<Expr> {
        // TODO: Evaluate binary operation on two integers
        // Return Some(result) if operation is valid, None otherwise
        // Handle Add, Sub, Mul, Div, Eq, Lt
        todo!()
    }

    fn eval_binary_bool(&self, op: BinaryOp, left: bool, right: bool) -> Option<Expr> {
        // TODO: Evaluate binary operation on two booleans
        // Handle And, Or, Eq
        todo!()
    }

    fn eval_unary(&self, op: UnaryOp, operand: &Expr) -> Option<Expr> {
        // TODO: Evaluate unary operation
        // Handle Neg (for integers) and Not (for booleans)
        todo!()
    }

    fn apply_algebraic_identity(&self, op: BinaryOp, left: &Expr, right: &Expr) -> Option<Expr> {
        // TODO: Apply algebraic identities
        // Examples:
        // - x + 0 → x, 0 + x → x
        // - x * 0 → 0, 0 * x → 0
        // - x * 1 → x, 1 * x → x
        // - x - 0 → x
        // - x && true → x, true && x → x
        // - x && false → false, false && x → false
        // - x || true → true, true || x → true
        // - x || false → x, false || x → x
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn int(n: i64) -> Expr {
        Expr::Int(n)
    }

    fn bool(b: bool) -> Expr {
        Expr::Bool(b)
    }

    fn var(s: &str) -> Expr {
        Expr::Var(s.to_string())
    }

    fn binary(op: BinaryOp, left: Expr, right: Expr) -> Expr {
        Expr::Binary {
            op,
            left: Box::new(left),
            right: Box::new(right),
        }
    }

    fn unary(op: UnaryOp, operand: Expr) -> Expr {
        Expr::Unary {
            op: op,
            operand: Box::new(operand),
        }
    }

    #[test]
    fn test_constant_arithmetic() {
        let folder = ConstantFolder::new();

        // 2 + 3 → 5
        let expr = binary(BinaryOp::Add, int(2), int(3));
        assert_eq!(folder.fold(expr), int(5));

        // 10 * 5 → 50
        let expr = binary(BinaryOp::Mul, int(10), int(5));
        assert_eq!(folder.fold(expr), int(50));

        // 20 - 7 → 13
        let expr = binary(BinaryOp::Sub, int(20), int(7));
        assert_eq!(folder.fold(expr), int(13));

        // 100 / 4 → 25
        let expr = binary(BinaryOp::Div, int(100), int(4));
        assert_eq!(folder.fold(expr), int(25));
    }

    #[test]
    fn test_nested_constants() {
        let folder = ConstantFolder::new();

        // (2 + 3) * 4 → 20
        let expr = binary(
            BinaryOp::Mul,
            binary(BinaryOp::Add, int(2), int(3)),
            int(4),
        );
        assert_eq!(folder.fold(expr), int(20));
    }

    #[test]
    fn test_identity_add_zero() {
        let folder = ConstantFolder::new();

        // x + 0 → x
        let expr = binary(BinaryOp::Add, var("x"), int(0));
        assert_eq!(folder.fold(expr), var("x"));

        // 0 + x → x
        let expr = binary(BinaryOp::Add, int(0), var("x"));
        assert_eq!(folder.fold(expr), var("x"));
    }

    #[test]
    fn test_identity_mul_zero() {
        let folder = ConstantFolder::new();

        // x * 0 → 0
        let expr = binary(BinaryOp::Mul, var("x"), int(0));
        assert_eq!(folder.fold(expr), int(0));

        // 0 * x → 0
        let expr = binary(BinaryOp::Mul, int(0), var("x"));
        assert_eq!(folder.fold(expr), int(0));
    }

    #[test]
    fn test_identity_mul_one() {
        let folder = ConstantFolder::new();

        // x * 1 → x
        let expr = binary(BinaryOp::Mul, var("x"), int(1));
        assert_eq!(folder.fold(expr), var("x"));

        // 1 * x → x
        let expr = binary(BinaryOp::Mul, int(1), var("x"));
        assert_eq!(folder.fold(expr), var("x"));
    }

    #[test]
    fn test_identity_sub_zero() {
        let folder = ConstantFolder::new();

        // x - 0 → x
        let expr = binary(BinaryOp::Sub, var("x"), int(0));
        assert_eq!(folder.fold(expr), var("x"));
    }

    #[test]
    fn test_boolean_constants() {
        let folder = ConstantFolder::new();

        // true && false → false
        let expr = binary(BinaryOp::And, bool(true), bool(false));
        assert_eq!(folder.fold(expr), bool(false));

        // true || false → true
        let expr = binary(BinaryOp::Or, bool(true), bool(false));
        assert_eq!(folder.fold(expr), bool(true));
    }

    #[test]
    fn test_boolean_identities() {
        let folder = ConstantFolder::new();

        // x && true → x
        let expr = binary(BinaryOp::And, var("x"), bool(true));
        assert_eq!(folder.fold(expr), var("x"));

        // x && false → false
        let expr = binary(BinaryOp::And, var("x"), bool(false));
        assert_eq!(folder.fold(expr), bool(false));

        // x || true → true
        let expr = binary(BinaryOp::Or, var("x"), bool(true));
        assert_eq!(folder.fold(expr), bool(true));

        // x || false → x
        let expr = binary(BinaryOp::Or, var("x"), bool(false));
        assert_eq!(folder.fold(expr), var("x"));
    }

    #[test]
    fn test_unary_negation() {
        let folder = ConstantFolder::new();

        // -5 → -5
        let expr = unary(UnaryOp::Neg, int(5));
        assert_eq!(folder.fold(expr), int(-5));

        // !true → false
        let expr = unary(UnaryOp::Not, bool(true));
        assert_eq!(folder.fold(expr), bool(false));

        // !false → true
        let expr = unary(UnaryOp::Not, bool(false));
        assert_eq!(folder.fold(expr), bool(true));
    }

    #[test]
    fn test_if_constant_condition() {
        let folder = ConstantFolder::new();

        // if true then 1 else 2 → 1
        let expr = Expr::If {
            condition: Box::new(bool(true)),
            then_branch: Box::new(int(1)),
            else_branch: Box::new(int(2)),
        };
        assert_eq!(folder.fold(expr), int(1));

        // if false then 1 else 2 → 2
        let expr = Expr::If {
            condition: Box::new(bool(false)),
            then_branch: Box::new(int(1)),
            else_branch: Box::new(int(2)),
        };
        assert_eq!(folder.fold(expr), int(2));
    }

    #[test]
    fn test_partial_folding() {
        let folder = ConstantFolder::new();

        // (2 + 3) + x → 5 + x
        let expr = binary(
            BinaryOp::Add,
            binary(BinaryOp::Add, int(2), int(3)),
            var("x"),
        );
        let expected = binary(BinaryOp::Add, int(5), var("x"));
        assert_eq!(folder.fold(expr), expected);
    }

    #[test]
    fn test_comparison_folding() {
        let folder = ConstantFolder::new();

        // 5 == 5 → true
        let expr = binary(BinaryOp::Eq, int(5), int(5));
        assert_eq!(folder.fold(expr), bool(true));

        // 5 == 6 → false
        let expr = binary(BinaryOp::Eq, int(5), int(6));
        assert_eq!(folder.fold(expr), bool(false));

        // 3 < 5 → true
        let expr = binary(BinaryOp::Lt, int(3), int(5));
        assert_eq!(folder.fold(expr), bool(true));
    }
}
