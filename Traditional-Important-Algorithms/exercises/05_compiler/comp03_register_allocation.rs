// comp03_register_allocation.rs
//
// Register allocation assigns virtual registers (unlimited) to physical
// registers (limited) using graph coloring. Variables that are live at
// the same time cannot share the same register - they interfere.
//
// Your task: Implement register allocation using graph coloring.
//
// Algorithm:
// 1. Build an interference graph where nodes are variables
// 2. Nodes are connected if variables are live simultaneously
// 3. Color the graph with K colors (K = number of physical registers)
// 4. If successful, each color represents a physical register

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct VarId(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RegisterId(pub usize);

pub struct InterferenceGraph {
    // Adjacency list representation
    edges: HashMap<VarId, HashSet<VarId>>,
}

impl InterferenceGraph {
    pub fn new() -> Self {
        Self {
            edges: HashMap::new(),
        }
    }

    pub fn add_variable(&mut self, var: VarId) {
        // TODO: Add a variable to the graph (with no edges initially)
        todo!()
    }

    pub fn add_interference(&mut self, var1: VarId, var2: VarId) {
        // TODO: Add an edge between two variables (undirected)
        // This means they interfere and cannot share a register
        todo!()
    }

    pub fn neighbors(&self, var: VarId) -> Vec<VarId> {
        // TODO: Return all neighbors (interfering variables) of var
        todo!()
    }

    pub fn degree(&self, var: VarId) -> usize {
        // TODO: Return the degree (number of neighbors) of var
        todo!()
    }

    pub fn remove_variable(&mut self, var: VarId) {
        // TODO: Remove a variable and all its edges from the graph
        todo!()
    }

    pub fn variables(&self) -> Vec<VarId> {
        // TODO: Return all variables in the graph
        todo!()
    }
}

pub struct RegisterAllocator {
    graph: InterferenceGraph,
    num_registers: usize,
}

impl RegisterAllocator {
    pub fn new(graph: InterferenceGraph, num_registers: usize) -> Self {
        Self {
            graph,
            num_registers,
        }
    }

    pub fn allocate(&mut self) -> Result<HashMap<VarId, RegisterId>, Vec<VarId>> {
        // TODO: Allocate registers using graph coloring
        // Return Ok(mapping) if successful, Err(spilled_vars) if we need to spill
        //
        // Algorithm:
        // 1. Build a stack by repeatedly removing nodes with degree < K
        // 2. If all remaining nodes have degree >= K, pick one to spill
        // 3. Color nodes by popping from stack and assigning colors
        // 4. A node can use any color not used by its neighbors
        todo!()
    }

    fn simplify(&mut self, stack: &mut Vec<VarId>) -> Option<VarId> {
        // TODO: Find a variable with degree < num_registers
        // Remove it from graph and push onto stack
        // Return Some(var) if found, None if all variables have high degree
        todo!()
    }

    fn color_graph(&self, stack: Vec<VarId>) -> Result<HashMap<VarId, RegisterId>, Vec<VarId>> {
        // TODO: Color the graph by processing variables in reverse stack order
        // For each variable, assign it a color not used by its neighbors
        // If no color available, add to spill list
        todo!()
    }

    fn find_available_register(
        &self,
        var: VarId,
        coloring: &HashMap<VarId, RegisterId>,
    ) -> Option<RegisterId> {
        // TODO: Find a register not used by any neighbor of var
        // Check neighbors, collect their colors, find first available
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_interference_graph() {
        let mut graph = InterferenceGraph::new();

        graph.add_variable(VarId(0));
        graph.add_variable(VarId(1));
        graph.add_variable(VarId(2));

        graph.add_interference(VarId(0), VarId(1));
        graph.add_interference(VarId(1), VarId(2));

        assert_eq!(graph.degree(VarId(0)), 1);
        assert_eq!(graph.degree(VarId(1)), 2);
        assert_eq!(graph.degree(VarId(2)), 1);

        assert_eq!(graph.neighbors(VarId(0)), vec![VarId(1)]);
    }

    #[test]
    fn test_simple_allocation() {
        // Three variables, no interference, should all get different registers
        let mut graph = InterferenceGraph::new();
        graph.add_variable(VarId(0));
        graph.add_variable(VarId(1));
        graph.add_variable(VarId(2));

        let mut allocator = RegisterAllocator::new(graph, 3);
        let result = allocator.allocate();

        assert!(result.is_ok());
        let mapping = result.unwrap();
        assert_eq!(mapping.len(), 3);
    }

    #[test]
    fn test_linear_interference() {
        // Variables: 0 - 1 - 2 (chain)
        // Can be colored with 2 registers
        let mut graph = InterferenceGraph::new();
        graph.add_variable(VarId(0));
        graph.add_variable(VarId(1));
        graph.add_variable(VarId(2));

        graph.add_interference(VarId(0), VarId(1));
        graph.add_interference(VarId(1), VarId(2));

        let mut allocator = RegisterAllocator::new(graph, 2);
        let result = allocator.allocate();

        assert!(result.is_ok());
        let mapping = result.unwrap();

        // var0 and var2 should get same register (no interference)
        // var1 should get different register
        assert_eq!(mapping[&VarId(0)], mapping[&VarId(2)]);
        assert_ne!(mapping[&VarId(0)], mapping[&VarId(1)]);
    }

    #[test]
    fn test_triangle_interference() {
        // Variables: 0 - 1 - 2 - 0 (triangle)
        // Needs 3 registers minimum
        let mut graph = InterferenceGraph::new();
        graph.add_variable(VarId(0));
        graph.add_variable(VarId(1));
        graph.add_variable(VarId(2));

        graph.add_interference(VarId(0), VarId(1));
        graph.add_interference(VarId(1), VarId(2));
        graph.add_interference(VarId(2), VarId(0));

        // With 3 registers, should succeed
        let mut allocator = RegisterAllocator::new(graph.clone(), 3);
        let result = allocator.allocate();
        assert!(result.is_ok());

        // With 2 registers, should fail (need to spill)
        let mut allocator = RegisterAllocator::new(graph, 2);
        let result = allocator.allocate();
        assert!(result.is_err());
    }

    #[test]
    fn test_complex_graph() {
        // More complex interference pattern
        let mut graph = InterferenceGraph::new();
        for i in 0..5 {
            graph.add_variable(VarId(i));
        }

        // Create a more complex pattern
        graph.add_interference(VarId(0), VarId(1));
        graph.add_interference(VarId(0), VarId(2));
        graph.add_interference(VarId(1), VarId(2));
        graph.add_interference(VarId(2), VarId(3));
        graph.add_interference(VarId(3), VarId(4));

        let mut allocator = RegisterAllocator::new(graph, 3);
        let result = allocator.allocate();

        assert!(result.is_ok());
        let mapping = result.unwrap();

        // Verify no interfering variables share a register
        assert_ne!(mapping[&VarId(0)], mapping[&VarId(1)]);
        assert_ne!(mapping[&VarId(0)], mapping[&VarId(2)]);
        assert_ne!(mapping[&VarId(1)], mapping[&VarId(2)]);
        assert_ne!(mapping[&VarId(2)], mapping[&VarId(3)]);
        assert_ne!(mapping[&VarId(3)], mapping[&VarId(4)]);
    }

    #[test]
    fn test_spilling() {
        // Complete graph K4 needs 4 colors
        let mut graph = InterferenceGraph::new();
        for i in 0..4 {
            graph.add_variable(VarId(i));
        }

        for i in 0..4 {
            for j in i+1..4 {
                graph.add_interference(VarId(i), VarId(j));
            }
        }

        // With 3 registers, must spill at least one variable
        let mut allocator = RegisterAllocator::new(graph, 3);
        let result = allocator.allocate();

        assert!(result.is_err());
        let spilled = result.unwrap_err();
        assert!(!spilled.is_empty());
    }
}
