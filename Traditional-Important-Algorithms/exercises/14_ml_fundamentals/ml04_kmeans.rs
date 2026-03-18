// ml04_kmeans.rs
//
// K-Means is an unsupervised clustering algorithm that partitions data into K clusters
// by iteratively assigning points to the nearest centroid and updating centroids.
//
// Key concepts:
// - Centroids: Mean position of all points in a cluster
// - Assignment step: Assign each point to nearest centroid (Euclidean distance)
// - Update step: Recompute centroids as mean of assigned points
// - Convergence: Algorithm stops when centroids don't change significantly
// - K-Means++: Smart initialization to improve convergence
//
// Your task: Implement K-Means clustering with random and K-Means++ initialization.
//
// Applications:
// - Customer segmentation
// - Image compression
// - Document clustering
// - Anomaly detection

// I AM NOT DONE

use std::collections::HashMap;

pub struct KMeans {
    k: usize,
    max_iterations: usize,
    centroids: Vec<Vec<f64>>,
}

impl KMeans {
    pub fn new(k: usize, max_iterations: usize) -> Self {
        Self {
            k,
            max_iterations,
            centroids: Vec::new(),
        }
    }

    fn euclidean_distance(a: &[f64], b: &[f64]) -> f64 {
        // TODO: Compute Euclidean distance: sqrt(sum((a_i - b_i)^2))
        todo!()
    }

    fn initialize_random(&mut self, data: &[Vec<f64>]) {
        // TODO: Randomly select K points from data as initial centroids
        // Hint: You can use the first K points for simplicity in tests
        // In practice, use random sampling
        todo!()
    }

    fn initialize_plus_plus(&mut self, data: &[Vec<f64>]) {
        // TODO: Implement K-Means++ initialization
        // 1. Choose first centroid randomly from data
        // 2. For each remaining centroid:
        //    a. For each point, compute distance to nearest existing centroid
        //    b. Choose next centroid with probability proportional to distance^2
        //    (Points far from existing centroids more likely to be chosen)
        // 3. This leads to better initial centroids and faster convergence
        //
        // For this exercise, you can use a simplified version:
        // Choose points with maximum distance to nearest centroid
        todo!()
    }

    fn assign_clusters(&self, data: &[Vec<f64>]) -> Vec<usize> {
        // TODO: Assign each data point to nearest centroid
        // Return vector of cluster indices (0 to k-1) for each point
        // For each point, find centroid with minimum Euclidean distance
        todo!()
    }

    fn update_centroids(&mut self, data: &[Vec<f64>], assignments: &[usize]) {
        // TODO: Update centroids as mean of assigned points
        // For each cluster:
        // 1. Find all points assigned to that cluster
        // 2. Compute mean of those points (average each dimension)
        // 3. Set that as new centroid
        // Handle empty clusters by keeping previous centroid
        todo!()
    }

    pub fn fit(&mut self, data: &[Vec<f64>], use_plus_plus: bool) {
        // TODO: Run K-Means algorithm
        // 1. Initialize centroids (random or K-Means++)
        // 2. Repeat until convergence or max_iterations:
        //    a. Assign each point to nearest centroid
        //    b. Update centroids
        //    c. Check for convergence (centroids don't change)
        todo!()
    }

    pub fn predict(&self, data: &[Vec<f64>]) -> Vec<usize> {
        // TODO: Assign new data points to existing clusters
        // Simply return result of assign_clusters
        todo!()
    }

    pub fn inertia(&self, data: &[Vec<f64>]) -> f64 {
        // TODO: Compute sum of squared distances to nearest centroid
        // Also called "within-cluster sum of squares" (WCSS)
        // Lower inertia means tighter clusters
        // inertia = sum over all points (distance to nearest centroid)^2
        todo!()
    }

    pub fn get_centroids(&self) -> &[Vec<f64>] {
        &self.centroids
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_eq(a: f64, b: f64, epsilon: f64) -> bool {
        (a - b).abs() < epsilon
    }

    #[test]
    fn test_euclidean_distance() {
        let a = vec![0.0, 0.0];
        let b = vec![3.0, 4.0];
        let dist = KMeans::euclidean_distance(&a, &b);
        assert!(approx_eq(dist, 5.0, 0.001));
    }

    #[test]
    fn test_distance_same_point() {
        let a = vec![1.0, 2.0, 3.0];
        let dist = KMeans::euclidean_distance(&a, &a);
        assert!(approx_eq(dist, 0.0, 0.001));
    }

    #[test]
    fn test_simple_clustering() {
        // Two clear clusters: around (0,0) and (10,10)
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![0.5, 0.5],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
            vec![10.5, 10.5],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        let assignments = kmeans.predict(&data);

        // First three should be in one cluster, last three in another
        assert_eq!(assignments[0], assignments[1]);
        assert_eq!(assignments[1], assignments[2]);
        assert_eq!(assignments[3], assignments[4]);
        assert_eq!(assignments[4], assignments[5]);
        assert_ne!(assignments[0], assignments[3]);
    }

    #[test]
    fn test_three_clusters() {
        // Three clusters: (0,0), (10,0), (5,10)
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 0.0],
            vec![10.0, 0.0],
            vec![11.0, 0.0],
            vec![5.0, 10.0],
            vec![5.0, 11.0],
        ];

        let mut kmeans = KMeans::new(3, 100);
        kmeans.fit(&data, false);

        let assignments = kmeans.predict(&data);

        // Points in each cluster should have same assignment
        assert_eq!(assignments[0], assignments[1]);
        assert_eq!(assignments[2], assignments[3]);
        assert_eq!(assignments[4], assignments[5]);

        // All three clusters should be different
        assert_ne!(assignments[0], assignments[2]);
        assert_ne!(assignments[0], assignments[4]);
        assert_ne!(assignments[2], assignments[4]);
    }

    #[test]
    fn test_centroids_count() {
        let data = vec![
            vec![1.0, 1.0],
            vec![2.0, 2.0],
            vec![8.0, 8.0],
            vec![9.0, 9.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        assert_eq!(kmeans.get_centroids().len(), 2);
    }

    #[test]
    fn test_centroid_positions() {
        // Simple case: points exactly at (0,0) and (10,10)
        let data = vec![
            vec![0.0, 0.0],
            vec![0.0, 0.0],
            vec![10.0, 10.0],
            vec![10.0, 10.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        let centroids = kmeans.get_centroids();

        // One centroid should be near (0,0), other near (10,10)
        let has_origin = centroids.iter().any(|c| {
            approx_eq(c[0], 0.0, 1.0) && approx_eq(c[1], 0.0, 1.0)
        });
        let has_far = centroids.iter().any(|c| {
            approx_eq(c[0], 10.0, 1.0) && approx_eq(c[1], 10.0, 1.0)
        });

        assert!(has_origin);
        assert!(has_far);
    }

    #[test]
    fn test_inertia() {
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        let inertia = kmeans.inertia(&data);

        // Inertia should be positive and relatively small for well-separated clusters
        assert!(inertia > 0.0);
        assert!(inertia < 20.0);
    }

    #[test]
    fn test_more_clusters_lower_inertia() {
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![5.0, 5.0],
            vec![6.0, 6.0],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
        ];

        let mut kmeans2 = KMeans::new(2, 100);
        kmeans2.fit(&data, false);
        let inertia2 = kmeans2.inertia(&data);

        let mut kmeans3 = KMeans::new(3, 100);
        kmeans3.fit(&data, false);
        let inertia3 = kmeans3.inertia(&data);

        // More clusters should have lower or equal inertia
        assert!(inertia3 <= inertia2);
    }

    #[test]
    fn test_predict_new_points() {
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        // New points near existing clusters
        let new_data = vec![
            vec![0.5, 0.5],  // Near first cluster
            vec![10.5, 10.5], // Near second cluster
        ];

        let predictions = kmeans.predict(&new_data);

        // Each new point should be assigned to different cluster
        assert_ne!(predictions[0], predictions[1]);
    }

    #[test]
    fn test_one_dimensional_data() {
        let data = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![10.0],
            vec![11.0],
            vec![12.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        let assignments = kmeans.predict(&data);

        // First three in one cluster, last three in another
        assert_eq!(assignments[0], assignments[1]);
        assert_eq!(assignments[1], assignments[2]);
        assert_eq!(assignments[3], assignments[4]);
        assert_eq!(assignments[4], assignments[5]);
        assert_ne!(assignments[0], assignments[3]);
    }

    #[test]
    fn test_kmeans_plus_plus() {
        let data = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, true); // Use K-Means++

        let assignments = kmeans.predict(&data);

        // Should still correctly cluster the data
        assert_eq!(assignments[0], assignments[1]);
        assert_eq!(assignments[2], assignments[3]);
        assert_ne!(assignments[0], assignments[2]);
    }

    #[test]
    fn test_high_dimensional() {
        // 4D data
        let data = vec![
            vec![0.0, 0.0, 0.0, 0.0],
            vec![1.0, 1.0, 1.0, 1.0],
            vec![10.0, 10.0, 10.0, 10.0],
            vec![11.0, 11.0, 11.0, 11.0],
        ];

        let mut kmeans = KMeans::new(2, 100);
        kmeans.fit(&data, false);

        let assignments = kmeans.predict(&data);

        assert_eq!(assignments[0], assignments[1]);
        assert_eq!(assignments[2], assignments[3]);
        assert_ne!(assignments[0], assignments[2]);
    }

    #[test]
    fn test_convergence() {
        let data = vec![
            vec![0.0, 0.0],
            vec![0.0, 0.0],
            vec![10.0, 10.0],
            vec![10.0, 10.0],
        ];

        let mut kmeans = KMeans::new(2, 1000);
        kmeans.fit(&data, false);

        // After convergence, predictions should be stable
        let pred1 = kmeans.predict(&data);
        let pred2 = kmeans.predict(&data);

        assert_eq!(pred1, pred2);
    }
}
