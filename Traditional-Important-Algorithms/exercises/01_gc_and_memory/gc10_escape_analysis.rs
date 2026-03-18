// gc10_escape_analysis.rs
//
// Escape analysis determines whether an object's lifetime is confined
// to a specific scope. Non-escaping objects can be stack-allocated,
// avoiding GC overhead.
//
// Your task: Implement a simple escape analysis for a toy language.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct VarId(usize);

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Alloc,                          // Allocate new object
    Var(VarId),                     // Variable reference
    Assign(VarId, Box<Expr>),       // x = expr
    Return(VarId),                  // return x
    Call(VarId, Vec<VarId>),        // f(x, y, z)
    Field(VarId, String),           // x.field
    StoreField(VarId, String, VarId), // x.field = y
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum EscapeStatus {
    NoEscape,      // Object doesn't escape
    ArgEscape,     // Escapes as function argument
    GlobalEscape,  // Escapes to global scope (return, store in global field)
}

pub struct EscapeAnalyzer {
    expressions: Vec<Expr>,
    var_status: HashMap<VarId, EscapeStatus>,
}

impl EscapeAnalyzer {
    pub fn new(expressions: Vec<Expr>) -> Self {
        Self {
            expressions,
            var_status: HashMap::new(),
        }
    }

    pub fn analyze(&mut self) {
        // TODO: Perform escape analysis on all expressions
        // Update var_status for each variable
        todo!()
    }

    fn analyze_expr(&mut self, expr: &Expr) {
        // TODO: Analyze a single expression
        // Update escape status based on how variables are used
        todo!()
    }

    fn mark_escape(&mut self, var: VarId, status: EscapeStatus) {
        // TODO: Mark a variable as escaping
        // If already marked with "worse" escape status, keep it
        // Order: NoEscape < ArgEscape < GlobalEscape
        todo!()
    }

    pub fn get_status(&self, var: VarId) -> Option<EscapeStatus> {
        self.var_status.get(&var).copied()
    }

    pub fn can_stack_allocate(&self, var: VarId) -> bool {
        // TODO: Return true if variable can be stack allocated
        // Only NoEscape variables can be stack allocated
        todo!()
    }

    pub fn escaping_vars(&self) -> Vec<VarId> {
        // TODO: Return all variables that escape (ArgEscape or GlobalEscape)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_escape() {
        let exprs = vec![
            Expr::Assign(VarId(0), Box::new(Expr::Alloc)),
            // x = new Object(); x doesn't escape
        ];

        let mut analyzer = EscapeAnalyzer::new(exprs);
        analyzer.analyze();

        assert_eq!(analyzer.get_status(VarId(0)), Some(EscapeStatus::NoEscape));
        assert_eq!(analyzer.can_stack_allocate(VarId(0)), true);
    }

    #[test]
    fn test_return_escape() {
        let exprs = vec![
            Expr::Assign(VarId(0), Box::new(Expr::Alloc)),
            Expr::Return(VarId(0)),
        ];

        let mut analyzer = EscapeAnalyzer::new(exprs);
        analyzer.analyze();

        assert_eq!(analyzer.get_status(VarId(0)), Some(EscapeStatus::GlobalEscape));
        assert_eq!(analyzer.can_stack_allocate(VarId(0)), false);
    }

    #[test]
    fn test_arg_escape() {
        let exprs = vec![
            Expr::Assign(VarId(0), Box::new(Expr::Alloc)),
            Expr::Call(VarId(1), vec![VarId(0)]),
        ];

        let mut analyzer = EscapeAnalyzer::new(exprs);
        analyzer.analyze();

        assert_eq!(analyzer.get_status(VarId(0)), Some(EscapeStatus::ArgEscape));
        assert_eq!(analyzer.can_stack_allocate(VarId(0)), false);
    }

    #[test]
    fn test_field_store_escape() {
        let exprs = vec![
            Expr::Assign(VarId(0), Box::new(Expr::Alloc)),
            Expr::Assign(VarId(1), Box::new(Expr::Alloc)),
            Expr::StoreField(VarId(0), "field".to_string(), VarId(1)),
        ];

        let mut analyzer = EscapeAnalyzer::new(exprs);
        analyzer.analyze();

        // VarId(1) escapes because it's stored in a field
        assert_eq!(analyzer.get_status(VarId(1)), Some(EscapeStatus::ArgEscape));
    }

    #[test]
    fn test_multiple_vars() {
        let exprs = vec![
            Expr::Assign(VarId(0), Box::new(Expr::Alloc)), // no escape
            Expr::Assign(VarId(1), Box::new(Expr::Alloc)), // returns
            Expr::Assign(VarId(2), Box::new(Expr::Alloc)), // arg escape
            Expr::Return(VarId(1)),
            Expr::Call(VarId(3), vec![VarId(2)]),
        ];

        let mut analyzer = EscapeAnalyzer::new(exprs);
        analyzer.analyze();

        assert!(analyzer.can_stack_allocate(VarId(0)));
        assert!(!analyzer.can_stack_allocate(VarId(1)));
        assert!(!analyzer.can_stack_allocate(VarId(2)));
    }
}
