// os07_banker_algorithm.rs
//
// The Banker's Algorithm is a deadlock avoidance algorithm that tests for safety by
// simulating the allocation of predetermined maximum possible amounts of all resources,
// and then makes a "safe state" check to test for possible deadlock conditions.
//
// Your task: Implement the Banker's Algorithm for deadlock avoidance.

// I AM NOT DONE

#[derive(Debug, Clone)]
pub struct BankerAlgorithm {
    num_processes: usize,
    num_resources: usize,
    // Available[j] = number of available instances of resource j
    available: Vec<usize>,
    // Maximum[i][j] = maximum demand of process i for resource j
    maximum: Vec<Vec<usize>>,
    // Allocation[i][j] = number of instances of resource j allocated to process i
    allocation: Vec<Vec<usize>>,
    // Need[i][j] = remaining need of process i for resource j
    need: Vec<Vec<usize>>,
}

impl BankerAlgorithm {
    pub fn new(
        num_processes: usize,
        num_resources: usize,
        available: Vec<usize>,
        maximum: Vec<Vec<usize>>,
    ) -> Self {
        // TODO: Initialize the Banker's Algorithm
        // 1. Create allocation matrix (all zeros initially)
        // 2. Calculate need matrix: Need[i][j] = Maximum[i][j] - Allocation[i][j]
        todo!()
    }

    pub fn request_resources(
        &mut self,
        process_id: usize,
        request: Vec<usize>,
    ) -> Result<(), &'static str> {
        // TODO: Process a resource request
        // 1. Check if request <= need[process_id]
        // 2. Check if request <= available
        // 3. Pretend to allocate resources
        // 4. Check if state is safe
        // 5. If safe, commit the allocation; otherwise, rollback
        todo!()
    }

    pub fn release_resources(
        &mut self,
        process_id: usize,
        release: Vec<usize>,
    ) -> Result<(), &'static str> {
        // TODO: Release resources from a process
        // 1. Check that release <= allocation[process_id]
        // 2. Update allocation and available
        // 3. Recalculate need
        todo!()
    }

    pub fn is_safe_state(&self) -> bool {
        // TODO: Implement the safety algorithm
        // 1. Create work vector = available
        // 2. Create finish vector (all false)
        // 3. Find process i where finish[i] == false and need[i] <= work
        // 4. If found: work += allocation[i], finish[i] = true, repeat step 3
        // 5. If all finish[i] == true, state is safe
        todo!()
    }

    fn find_safe_sequence(&self) -> Option<Vec<usize>> {
        // TODO: Find a safe sequence of process execution
        // Return the sequence if one exists, None otherwise
        // This is similar to is_safe_state but returns the actual sequence
        todo!()
    }

    pub fn get_available(&self) -> &[usize] {
        &self.available
    }

    pub fn get_allocation(&self, process_id: usize) -> Option<&[usize]> {
        self.allocation.get(process_id).map(|v| v.as_slice())
    }

    pub fn get_need(&self, process_id: usize) -> Option<&[usize]> {
        self.need.get(process_id).map(|v| v.as_slice())
    }

    pub fn get_maximum(&self, process_id: usize) -> Option<&[usize]> {
        self.maximum.get(process_id).map(|v| v.as_slice())
    }

    fn calculate_need(&mut self) {
        // TODO: Recalculate the need matrix
        // Need[i][j] = Maximum[i][j] - Allocation[i][j]
        todo!()
    }

    pub fn deadlock_would_occur(&self, process_id: usize, request: &[usize]) -> bool {
        // TODO: Check if granting this request would lead to deadlock
        // Simulate the allocation and check if resulting state is safe
        todo!()
    }

    pub fn total_resources_allocated(&self) -> Vec<usize> {
        // TODO: Calculate total resources currently allocated across all processes
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_safe_state() {
        // Classic example from textbooks
        let available = vec![3, 3, 2];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
            vec![9, 0, 2],
            vec![2, 2, 2],
            vec![4, 3, 3],
        ];

        let banker = BankerAlgorithm::new(5, 3, available, maximum);

        assert!(banker.is_safe_state());
    }

    #[test]
    fn test_safe_request() {
        let available = vec![3, 3, 2];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
            vec![9, 0, 2],
            vec![2, 2, 2],
            vec![4, 3, 3],
        ];

        let mut banker = BankerAlgorithm::new(5, 3, available, maximum);

        // Process 1 requests (1, 0, 2)
        let result = banker.request_resources(1, vec![1, 0, 2]);
        assert!(result.is_ok());
    }

    #[test]
    fn test_unsafe_request() {
        let available = vec![3, 3, 2];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
            vec![9, 0, 2],
            vec![2, 2, 2],
            vec![4, 3, 3],
        ];

        let mut banker = BankerAlgorithm::new(5, 3, available, maximum);

        // Request that would make state unsafe
        let result = banker.request_resources(0, vec![4, 4, 3]);
        assert!(result.is_err());
    }

    #[test]
    fn test_request_exceeds_need() {
        let available = vec![3, 3, 2];
        let maximum = vec![vec![2, 2, 2]];

        let mut banker = BankerAlgorithm::new(1, 3, available, maximum);

        // Request more than maximum need
        let result = banker.request_resources(0, vec![3, 3, 3]);
        assert!(result.is_err());
    }

    #[test]
    fn test_request_exceeds_available() {
        let available = vec![1, 1, 1];
        let maximum = vec![vec![5, 5, 5]];

        let mut banker = BankerAlgorithm::new(1, 3, available, maximum);

        // Request more than available
        let result = banker.request_resources(0, vec![2, 2, 2]);
        assert!(result.is_err());
    }

    #[test]
    fn test_release_resources() {
        let available = vec![3, 3, 2];
        let maximum = vec![vec![5, 5, 5]];

        let mut banker = BankerAlgorithm::new(1, 3, available, maximum);

        // Allocate some resources
        banker.request_resources(0, vec![2, 2, 1]).unwrap();

        let before_available = banker.get_available().to_vec();

        // Release resources
        banker.release_resources(0, vec![1, 1, 1]).unwrap();

        let after_available = banker.get_available();

        assert_eq!(after_available[0], before_available[0] + 1);
        assert_eq!(after_available[1], before_available[1] + 1);
        assert_eq!(after_available[2], before_available[2] + 1);
    }

    #[test]
    fn test_multiple_processes() {
        let available = vec![10, 5, 7];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
            vec![9, 0, 2],
        ];

        let mut banker = BankerAlgorithm::new(3, 3, available, maximum);

        // Multiple processes request resources
        banker.request_resources(0, vec![0, 1, 0]).unwrap();
        banker.request_resources(1, vec![2, 0, 0]).unwrap();
        banker.request_resources(2, vec![3, 0, 2]).unwrap();

        assert!(banker.is_safe_state());
    }

    #[test]
    fn test_need_calculation() {
        let available = vec![3, 3, 2];
        let maximum = vec![vec![7, 5, 3]];

        let mut banker = BankerAlgorithm::new(1, 3, available, maximum);

        banker.request_resources(0, vec![2, 2, 1]).unwrap();

        let need = banker.get_need(0).unwrap();

        assert_eq!(need[0], 5); // 7 - 2
        assert_eq!(need[1], 3); // 5 - 2
        assert_eq!(need[2], 2); // 3 - 1
    }

    #[test]
    fn test_deadlock_detection() {
        let available = vec![2, 2, 2];
        let maximum = vec![
            vec![5, 5, 5],
            vec![5, 5, 5],
        ];

        let mut banker = BankerAlgorithm::new(2, 3, available, maximum);

        banker.request_resources(0, vec![2, 2, 2]).unwrap();

        // This request would likely cause deadlock
        assert!(banker.deadlock_would_occur(1, &vec![2, 2, 2]));
    }

    #[test]
    fn test_total_resources() {
        let available = vec![3, 3, 2];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
        ];

        let mut banker = BankerAlgorithm::new(2, 3, available, maximum);

        banker.request_resources(0, vec![1, 1, 1]).unwrap();
        banker.request_resources(1, vec![2, 1, 0]).unwrap();

        let total = banker.total_resources_allocated();

        assert_eq!(total[0], 3); // 1 + 2
        assert_eq!(total[1], 2); // 1 + 1
        assert_eq!(total[2], 1); // 1 + 0
    }

    #[test]
    fn test_safe_sequence_exists() {
        let available = vec![3, 3, 2];
        let maximum = vec![
            vec![7, 5, 3],
            vec![3, 2, 2],
            vec![9, 0, 2],
        ];

        let banker = BankerAlgorithm::new(3, 3, available, maximum);

        let sequence = banker.find_safe_sequence();
        assert!(sequence.is_some());

        if let Some(seq) = sequence {
            assert_eq!(seq.len(), 3);
        }
    }

    #[test]
    fn test_complete_workflow() {
        let available = vec![10, 10, 10];
        let maximum = vec![
            vec![5, 5, 5],
            vec![4, 4, 4],
            vec![3, 3, 3],
        ];

        let mut banker = BankerAlgorithm::new(3, 3, available, maximum);

        // Process 0 requests and gets resources
        banker.request_resources(0, vec![2, 2, 2]).unwrap();
        assert_eq!(banker.get_allocation(0).unwrap(), &[2, 2, 2]);

        // Process 1 requests and gets resources
        banker.request_resources(1, vec![3, 3, 3]).unwrap();
        assert_eq!(banker.get_allocation(1).unwrap(), &[3, 3, 3]);

        // Process 0 completes and releases
        banker.release_resources(0, vec![2, 2, 2]).unwrap();
        assert_eq!(banker.get_allocation(0).unwrap(), &[0, 0, 0]);

        // More resources available now
        let available = banker.get_available();
        assert_eq!(available[0], 7); // 10 - 3 (for process 1)
    }
}
