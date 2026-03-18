// comp06_escape_analysis.rs
//
// Escape analysis determines whether an object's lifetime is confined
// to a specific scope. Non-escaping objects can be stack-allocated,
// avoiding heap allocation overhead.
//
// Your task: Implement a simple escape analysis for method calls.
//
// An object escapes if:
// - It is returned from a method
// - It is stored in a field
// - It is passed to another method
//
// Otherwise, it can be stack-allocated.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(pub usize);

#[derive(Debug, Clone, PartialEq)]
pub enum Instruction {
    // Create a new object
    New(ObjectId),

    // Store object in a field: objects[target].field = source
    StoreField {
        target: ObjectId,
        field: String,
        source: ObjectId,
    },

    // Load object from a field: dest = objects[source].field
    LoadField {
        dest: ObjectId,
        source: ObjectId,
        field: String,
    },

    // Call a method: result = method(args...)
    Call {
        result: Option<ObjectId>,
        method: String,
        args: Vec<ObjectId>,
    },

    // Return an object from the method
    Return(ObjectId),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EscapeState {
    NoEscape,        // Object doesn't escape - can be stack allocated
    ArgEscape,       // Object escapes as method argument - may escape
    GlobalEscape,    // Object escapes globally - definitely heap allocated
}

pub struct EscapeAnalysis {
    instructions: Vec<Instruction>,
    escape_states: HashMap<ObjectId, EscapeState>,
}

impl EscapeAnalysis {
    pub fn new(instructions: Vec<Instruction>) -> Self {
        Self {
            instructions,
            escape_states: HashMap::new(),
        }
    }

    pub fn analyze(&mut self) {
        // TODO: Analyze all instructions and determine escape state for each object
        // Start by marking all objects as NoEscape, then upgrade as needed
        todo!()
    }

    fn initialize_objects(&mut self) {
        // TODO: Find all New instructions and initialize their escape state to NoEscape
        todo!()
    }

    fn analyze_instruction(&mut self, instr: &Instruction) {
        // TODO: Analyze a single instruction and update escape states
        // - StoreField: source escapes to at least ArgEscape
        // - Call: arguments escape to at least ArgEscape
        // - Return: returned object escapes to GlobalEscape
        todo!()
    }

    fn mark_escape(&mut self, obj: ObjectId, new_state: EscapeState) {
        // TODO: Update escape state for an object
        // Only upgrade state (NoEscape -> ArgEscape -> GlobalEscape)
        // Never downgrade
        todo!()
    }

    pub fn get_escape_state(&self, obj: ObjectId) -> Option<EscapeState> {
        // TODO: Return the escape state of an object
        todo!()
    }

    pub fn can_stack_allocate(&self, obj: ObjectId) -> bool {
        // TODO: Return true if object can be stack allocated
        // Only NoEscape objects can be stack allocated
        todo!()
    }

    pub fn stack_allocatable_objects(&self) -> Vec<ObjectId> {
        // TODO: Return all objects that can be stack allocated
        todo!()
    }

    pub fn escaping_objects(&self) -> Vec<ObjectId> {
        // TODO: Return all objects that escape (ArgEscape or GlobalEscape)
        todo!()
    }

    pub fn propagate_escape(&mut self) {
        // TODO: Propagate escape information through field stores
        // If an object A is stored in field of object B, and B escapes,
        // then A must also escape at least as much as B
        //
        // This requires multiple passes until fixpoint
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_escape() {
        // Object is created but never used
        let instructions = vec![
            Instruction::New(ObjectId(0)),
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::NoEscape));
        assert!(analysis.can_stack_allocate(ObjectId(0)));
    }

    #[test]
    fn test_return_escape() {
        // Object is returned - global escape
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::Return(ObjectId(0)),
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::GlobalEscape));
        assert!(!analysis.can_stack_allocate(ObjectId(0)));
    }

    #[test]
    fn test_method_call_escape() {
        // Object is passed to method - arg escape
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::Call {
                result: None,
                method: "foo".to_string(),
                args: vec![ObjectId(0)],
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::ArgEscape));
        assert!(!analysis.can_stack_allocate(ObjectId(0)));
    }

    #[test]
    fn test_field_store_escape() {
        // Object is stored in field - arg escape
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::New(ObjectId(1)),
            Instruction::StoreField {
                target: ObjectId(0),
                field: "f".to_string(),
                source: ObjectId(1),
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        // Object 1 is stored in object 0's field, so it escapes
        assert_eq!(analysis.get_escape_state(ObjectId(1)), Some(EscapeState::ArgEscape));
    }

    #[test]
    fn test_multiple_objects() {
        let instructions = vec![
            Instruction::New(ObjectId(0)),  // No escape
            Instruction::New(ObjectId(1)),  // Returned
            Instruction::New(ObjectId(2)),  // Used in call
            Instruction::Return(ObjectId(1)),
            Instruction::Call {
                result: None,
                method: "process".to_string(),
                args: vec![ObjectId(2)],
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::NoEscape));
        assert_eq!(analysis.get_escape_state(ObjectId(1)), Some(EscapeState::GlobalEscape));
        assert_eq!(analysis.get_escape_state(ObjectId(2)), Some(EscapeState::ArgEscape));

        assert!(analysis.can_stack_allocate(ObjectId(0)));
        assert!(!analysis.can_stack_allocate(ObjectId(1)));
        assert!(!analysis.can_stack_allocate(ObjectId(2)));
    }

    #[test]
    fn test_transitive_escape() {
        // Object 2 is stored in object 1, which is stored in object 0, which is returned
        // So all should eventually escape
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::New(ObjectId(1)),
            Instruction::New(ObjectId(2)),
            Instruction::StoreField {
                target: ObjectId(1),
                field: "inner".to_string(),
                source: ObjectId(2),
            },
            Instruction::StoreField {
                target: ObjectId(0),
                field: "middle".to_string(),
                source: ObjectId(1),
            },
            Instruction::Return(ObjectId(0)),
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();
        analysis.propagate_escape(); // Need to propagate through field stores

        // All objects should escape since obj0 is returned
        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::GlobalEscape));

        // Depending on implementation, these might be ArgEscape or GlobalEscape
        // At minimum they should not be NoEscape
        assert_ne!(analysis.get_escape_state(ObjectId(1)), Some(EscapeState::NoEscape));
        assert_ne!(analysis.get_escape_state(ObjectId(2)), Some(EscapeState::NoEscape));
    }

    #[test]
    fn test_local_use_only() {
        // Object is created, has field accessed, but never escapes
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::New(ObjectId(1)),
            Instruction::LoadField {
                dest: ObjectId(1),
                source: ObjectId(0),
                field: "value".to_string(),
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        // LoadField doesn't cause escape - just reading
        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::NoEscape));
    }

    #[test]
    fn test_call_result() {
        // Result from method call doesn't escape
        let instructions = vec![
            Instruction::Call {
                result: Some(ObjectId(0)),
                method: "create".to_string(),
                args: vec![],
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        // Object returned from call starts as NoEscape in this context
        // (it may have escaped in the callee, but we don't know)
        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::NoEscape));
    }

    #[test]
    fn test_multiple_calls() {
        let instructions = vec![
            Instruction::New(ObjectId(0)),
            Instruction::Call {
                result: None,
                method: "process".to_string(),
                args: vec![ObjectId(0)],
            },
            Instruction::Call {
                result: None,
                method: "finalize".to_string(),
                args: vec![ObjectId(0)],
            },
        ];

        let mut analysis = EscapeAnalysis::new(instructions);
        analysis.analyze();

        // Passed to multiple methods - still ArgEscape
        assert_eq!(analysis.get_escape_state(ObjectId(0)), Some(EscapeState::ArgEscape));
    }
}
