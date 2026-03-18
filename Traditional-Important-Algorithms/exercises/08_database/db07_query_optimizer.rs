// db07_query_optimizer.rs
//
// Query Optimization is the process of selecting the most efficient execution plan
// for a query. The optimizer considers:
// - Join ordering (which tables to join first)
// - Index selection (which indexes to use)
// - Access methods (sequential scan vs index scan)
// - Cost estimation (I/O, CPU, memory)
//
// A simple cost model:
// - Sequential scan: cost = number of rows
// - Index scan: cost = log(number of rows) + matching rows
// - Join: cost = (rows in left table) * (rows in right table) / selectivity
//
// Your task: Implement a simple query optimizer with join ordering and index selection.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum ScanType {
    Sequential,
    IndexScan { index_name: String },
}

#[derive(Debug, Clone)]
pub struct TableStats {
    pub name: String,
    pub row_count: usize,
    pub indexes: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct QueryPlan {
    pub scan_type: ScanType,
    pub table: String,
    pub estimated_cost: f64,
}

#[derive(Debug, Clone)]
pub struct JoinPlan {
    pub left: Box<QueryPlan>,
    pub right: Box<QueryPlan>,
    pub join_column: String,
    pub estimated_cost: f64,
}

pub struct QueryOptimizer {
    table_stats: HashMap<String, TableStats>,
}

impl QueryOptimizer {
    pub fn new() -> Self {
        Self {
            table_stats: HashMap::new(),
        }
    }

    pub fn add_table(&mut self, stats: TableStats) {
        self.table_stats.insert(stats.name.clone(), stats);
    }

    pub fn optimize_scan(&self, table: &str, filter_column: Option<&str>) -> QueryPlan {
        // TODO: Choose between sequential scan and index scan
        // If filter_column is None, use sequential scan
        // If filter_column has an index, use index scan
        // Calculate estimated cost for each option
        // Return the plan with lower cost
        todo!()
    }

    pub fn optimize_join(&self, left_table: &str, right_table: &str, join_column: &str) -> JoinPlan {
        // TODO: Optimize a two-table join
        // Create plans for both tables
        // Estimate join cost based on row counts
        // Consider using indexes on join column
        todo!()
    }

    pub fn optimize_multi_join(&self, tables: Vec<&str>, join_columns: Vec<&str>) -> Vec<JoinPlan> {
        // TODO: Optimize joins for multiple tables
        // Consider different join orders
        // Use dynamic programming or greedy approach
        // Start with smallest tables first (greedy heuristic)
        // Return sequence of join operations
        todo!()
    }

    fn estimate_scan_cost(&self, table: &str, scan_type: &ScanType) -> f64 {
        // TODO: Estimate cost of scanning a table
        // Sequential: linear in row count
        // Index: logarithmic in row count + selectivity
        todo!()
    }

    fn estimate_join_cost(&self, left_rows: usize, right_rows: usize, selectivity: f64) -> f64 {
        // TODO: Estimate cost of joining two tables
        // Simple model: left_rows * right_rows * selectivity
        // Add costs of scanning both tables
        todo!()
    }

    pub fn get_table_stats(&self, table: &str) -> Option<&TableStats> {
        self.table_stats.get(table)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_optimizer() {
        let optimizer = QueryOptimizer::new();
        assert!(optimizer.get_table_stats("users").is_none());
    }

    #[test]
    fn test_add_table_stats() {
        let mut optimizer = QueryOptimizer::new();
        let stats = TableStats {
            name: "users".to_string(),
            row_count: 1000,
            indexes: vec!["id".to_string()],
        };
        optimizer.add_table(stats);

        let retrieved = optimizer.get_table_stats("users");
        assert!(retrieved.is_some());
        assert_eq!(retrieved.unwrap().row_count, 1000);
    }

    #[test]
    fn test_optimize_scan_without_index() {
        let mut optimizer = QueryOptimizer::new();
        optimizer.add_table(TableStats {
            name: "users".to_string(),
            row_count: 1000,
            indexes: vec![],
        });

        let plan = optimizer.optimize_scan("users", Some("name"));
        assert_eq!(plan.scan_type, ScanType::Sequential);
    }

    #[test]
    fn test_optimize_scan_with_index() {
        let mut optimizer = QueryOptimizer::new();
        optimizer.add_table(TableStats {
            name: "users".to_string(),
            row_count: 10000,
            indexes: vec!["email".to_string()],
        });

        let plan = optimizer.optimize_scan("users", Some("email"));
        assert!(matches!(plan.scan_type, ScanType::IndexScan { .. }));
    }

    #[test]
    fn test_sequential_scan_for_small_table() {
        let mut optimizer = QueryOptimizer::new();
        optimizer.add_table(TableStats {
            name: "small_table".to_string(),
            row_count: 10,
            indexes: vec!["id".to_string()],
        });

        let plan = optimizer.optimize_scan("small_table", None);
        // For small tables, sequential scan might be preferred even with index
        assert!(plan.estimated_cost > 0.0);
    }

    #[test]
    fn test_optimize_simple_join() {
        let mut optimizer = QueryOptimizer::new();

        optimizer.add_table(TableStats {
            name: "users".to_string(),
            row_count: 1000,
            indexes: vec!["id".to_string()],
        });

        optimizer.add_table(TableStats {
            name: "orders".to_string(),
            row_count: 5000,
            indexes: vec!["user_id".to_string()],
        });

        let plan = optimizer.optimize_join("users", "orders", "user_id");
        assert!(plan.estimated_cost > 0.0);
    }

    #[test]
    fn test_join_order_matters() {
        let mut optimizer = QueryOptimizer::new();

        optimizer.add_table(TableStats {
            name: "small".to_string(),
            row_count: 100,
            indexes: vec![],
        });

        optimizer.add_table(TableStats {
            name: "large".to_string(),
            row_count: 10000,
            indexes: vec![],
        });

        let plan1 = optimizer.optimize_join("small", "large", "id");
        let plan2 = optimizer.optimize_join("large", "small", "id");

        // Join order can affect cost
        assert!(plan1.estimated_cost > 0.0);
        assert!(plan2.estimated_cost > 0.0);
    }

    #[test]
    fn test_optimize_multi_join_three_tables() {
        let mut optimizer = QueryOptimizer::new();

        optimizer.add_table(TableStats {
            name: "users".to_string(),
            row_count: 1000,
            indexes: vec!["id".to_string()],
        });

        optimizer.add_table(TableStats {
            name: "orders".to_string(),
            row_count: 5000,
            indexes: vec!["user_id".to_string(), "product_id".to_string()],
        });

        optimizer.add_table(TableStats {
            name: "products".to_string(),
            row_count: 500,
            indexes: vec!["id".to_string()],
        });

        let plans = optimizer.optimize_multi_join(
            vec!["users", "orders", "products"],
            vec!["user_id", "product_id"],
        );

        assert!(!plans.is_empty());
    }

    #[test]
    fn test_index_selection_with_multiple_indexes() {
        let mut optimizer = QueryOptimizer::new();
        optimizer.add_table(TableStats {
            name: "users".to_string(),
            row_count: 10000,
            indexes: vec!["email".to_string(), "username".to_string(), "id".to_string()],
        });

        let plan = optimizer.optimize_scan("users", Some("email"));
        if let ScanType::IndexScan { index_name } = plan.scan_type {
            assert_eq!(index_name, "email");
        }
    }

    #[test]
    fn test_cost_estimation_increases_with_size() {
        let mut optimizer = QueryOptimizer::new();

        optimizer.add_table(TableStats {
            name: "small".to_string(),
            row_count: 100,
            indexes: vec![],
        });

        optimizer.add_table(TableStats {
            name: "large".to_string(),
            row_count: 100000,
            indexes: vec![],
        });

        let plan_small = optimizer.optimize_scan("small", None);
        let plan_large = optimizer.optimize_scan("large", None);

        assert!(plan_large.estimated_cost > plan_small.estimated_cost);
    }

    #[test]
    fn test_multi_join_optimal_order() {
        let mut optimizer = QueryOptimizer::new();

        optimizer.add_table(TableStats {
            name: "tiny".to_string(),
            row_count: 10,
            indexes: vec![],
        });

        optimizer.add_table(TableStats {
            name: "medium".to_string(),
            row_count: 1000,
            indexes: vec![],
        });

        optimizer.add_table(TableStats {
            name: "huge".to_string(),
            row_count: 1000000,
            indexes: vec![],
        });

        let plans = optimizer.optimize_multi_join(
            vec!["tiny", "medium", "huge"],
            vec!["id", "id"],
        );

        // Optimal order should start with smallest tables
        assert!(!plans.is_empty());
    }

    #[test]
    fn test_no_table_stats() {
        let optimizer = QueryOptimizer::new();
        assert!(optimizer.get_table_stats("nonexistent").is_none());
    }
}
