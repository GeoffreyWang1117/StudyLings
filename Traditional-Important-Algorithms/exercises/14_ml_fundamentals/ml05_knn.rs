// ml05_knn.rs
//
// K-Nearest Neighbors (KNN) is a simple, non-parametric algorithm that classifies
// data points based on the majority class of their K nearest neighbors.
//
// Key concepts:
// - Distance metric: Usually Euclidean distance
// - K parameter: Number of neighbors to consider (odd numbers avoid ties)
// - Lazy learning: No training phase, all computation at prediction time
// - Voting: Majority vote (classification) or average (regression)
// - Curse of dimensionality: Performance degrades in high dimensions
//
// Your task: Implement KNN for classification and regression.
//
// Applications:
// - Recommendation systems
// - Pattern recognition
// - Anomaly detection
// - Missing value imputation

// I AM NOT DONE

use std::collections::HashMap;

pub struct KNNClassifier {
    k: usize,
    x_train: Vec<Vec<f64>>,
    y_train: Vec<usize>,
}

impl KNNClassifier {
    pub fn new(k: usize) -> Self {
        Self {
            k,
            x_train: Vec::new(),
            y_train: Vec::new(),
        }
    }

    pub fn fit(&mut self, x: Vec<Vec<f64>>, y: Vec<usize>) {
        // TODO: Store training data
        // KNN is lazy learning - just save the data
        // No actual training computation needed
        todo!()
    }

    fn euclidean_distance(a: &[f64], b: &[f64]) -> f64 {
        // TODO: Compute Euclidean distance
        // sqrt(sum((a_i - b_i)^2))
        todo!()
    }

    fn manhattan_distance(a: &[f64], b: &[f64]) -> f64 {
        // TODO: Compute Manhattan distance
        // sum(|a_i - b_i|)
        todo!()
    }

    fn find_k_nearest(&self, point: &[f64]) -> Vec<usize> {
        // TODO: Find K nearest neighbors
        // 1. Compute distance from point to all training samples
        // 2. Sort by distance
        // 3. Return indices of K nearest samples
        // Hint: Create vec of (index, distance) pairs, sort, take first K
        todo!()
    }

    pub fn predict_one(&self, point: &[f64]) -> usize {
        // TODO: Predict class for a single point
        // 1. Find K nearest neighbors
        // 2. Get their labels
        // 3. Return most common label (majority vote)
        // Hint: Use HashMap to count votes
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>]) -> Vec<usize> {
        // TODO: Predict classes for multiple points
        // Apply predict_one to each point
        todo!()
    }

    pub fn accuracy(&self, x: &[Vec<f64>], y: &[usize]) -> f64 {
        // TODO: Compute classification accuracy
        // (number of correct predictions) / (total predictions)
        todo!()
    }
}

pub struct KNNRegressor {
    k: usize,
    x_train: Vec<Vec<f64>>,
    y_train: Vec<f64>,
}

impl KNNRegressor {
    pub fn new(k: usize) -> Self {
        Self {
            k,
            x_train: Vec::new(),
            y_train: Vec::new(),
        }
    }

    pub fn fit(&mut self, x: Vec<Vec<f64>>, y: Vec<f64>) {
        // TODO: Store training data
        todo!()
    }

    fn euclidean_distance(a: &[f64], b: &[f64]) -> f64 {
        // TODO: Compute Euclidean distance
        todo!()
    }

    fn find_k_nearest(&self, point: &[f64]) -> Vec<usize> {
        // TODO: Find K nearest neighbors (same as classifier)
        todo!()
    }

    pub fn predict_one(&self, point: &[f64]) -> f64 {
        // TODO: Predict value for a single point
        // 1. Find K nearest neighbors
        // 2. Get their target values
        // 3. Return average (mean) of those values
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>]) -> Vec<f64> {
        // TODO: Predict values for multiple points
        todo!()
    }

    pub fn mean_squared_error(&self, x: &[Vec<f64>], y: &[f64]) -> f64 {
        // TODO: Compute MSE
        // (1/n) * sum((predicted - actual)^2)
        todo!()
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
        assert!(approx_eq(KNNClassifier::euclidean_distance(&a, &b), 5.0, 0.001));
    }

    #[test]
    fn test_manhattan_distance() {
        let a = vec![0.0, 0.0];
        let b = vec![3.0, 4.0];
        assert!(approx_eq(KNNClassifier::manhattan_distance(&a, &b), 7.0, 0.001));
    }

    #[test]
    fn test_simple_classification() {
        // Two clusters: class 0 near origin, class 1 near (10,10)
        let x_train = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![0.5, 0.5],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
            vec![10.5, 10.5],
        ];
        let y_train = vec![0, 0, 0, 1, 1, 1];

        let mut knn = KNNClassifier::new(3);
        knn.fit(x_train, y_train);

        // Test points
        let x_test = vec![vec![0.2, 0.2], vec![10.2, 10.2]];
        let predictions = knn.predict(&x_test);

        assert_eq!(predictions[0], 0);
        assert_eq!(predictions[1], 1);
    }

    #[test]
    fn test_k1_classification() {
        // With K=1, should exactly match nearest neighbor
        let x_train = vec![
            vec![0.0, 0.0],
            vec![5.0, 5.0],
            vec![10.0, 10.0],
        ];
        let y_train = vec![0, 1, 2];

        let mut knn = KNNClassifier::new(1);
        knn.fit(x_train, y_train);

        // Point very close to (5,5) should be class 1
        let prediction = knn.predict_one(&vec![5.1, 5.1]);
        assert_eq!(prediction, 1);
    }

    #[test]
    fn test_majority_voting() {
        // Set up where K=3 gives different result than K=1
        let x_train = vec![
            vec![0.0, 0.0],  // class 0
            vec![1.0, 0.0],  // class 0
            vec![0.5, 0.1],  // class 0
            vec![0.6, 0.2],  // class 1 (closer but outvoted)
        ];
        let y_train = vec![0, 0, 0, 1];

        let mut knn = KNNClassifier::new(3);
        knn.fit(x_train, y_train);

        // Point near (0.6, 0.2) but should be class 0 due to majority
        let prediction = knn.predict_one(&vec![0.7, 0.3]);
        assert_eq!(prediction, 0);
    }

    #[test]
    fn test_accuracy() {
        let x_train = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
            vec![10.0, 10.0],
            vec![11.0, 11.0],
        ];
        let y_train = vec![0, 0, 1, 1];

        let mut knn = KNNClassifier::new(1);
        knn.fit(x_train.clone(), y_train.clone());

        let accuracy = knn.accuracy(&x_train, &y_train);
        assert_eq!(accuracy, 1.0); // Should perfectly fit training data
    }

    #[test]
    fn test_simple_regression() {
        // Simple pattern: y = x
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![4.0],
        ];
        let y_train = vec![1.0, 2.0, 3.0, 4.0];

        let mut knn = KNNRegressor::new(2);
        knn.fit(x_train, y_train);

        // Predict at x=2.5, should be close to 2.5
        let prediction = knn.predict_one(&vec![2.5]);
        assert!(approx_eq(prediction, 2.5, 0.5));
    }

    #[test]
    fn test_regression_averaging() {
        // y = x
        let x_train = vec![
            vec![1.0],
            vec![3.0],
        ];
        let y_train = vec![1.0, 3.0];

        let mut knn = KNNRegressor::new(2);
        knn.fit(x_train, y_train);

        // At x=2.0, both neighbors have equal distance
        // Average of 1.0 and 3.0 should be 2.0
        let prediction = knn.predict_one(&vec![2.0]);
        assert!(approx_eq(prediction, 2.0, 0.1));
    }

    #[test]
    fn test_regression_batch_predict() {
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
        ];
        let y_train = vec![2.0, 4.0, 6.0]; // y = 2x

        let mut knn = KNNRegressor::new(2);
        knn.fit(x_train, y_train);

        let x_test = vec![vec![1.5], vec![2.5]];
        let predictions = knn.predict(&x_test);

        assert_eq!(predictions.len(), 2);
        assert!(approx_eq(predictions[0], 3.0, 1.0));
        assert!(approx_eq(predictions[1], 5.0, 1.0));
    }

    #[test]
    fn test_regression_mse() {
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
        ];
        let y_train = vec![1.0, 2.0, 3.0];

        let mut knn = KNNRegressor::new(2);
        knn.fit(x_train.clone(), y_train.clone());

        let mse = knn.mean_squared_error(&x_train, &y_train);
        // With training data, MSE should be small
        assert!(mse < 1.0);
    }

    #[test]
    fn test_multiclass_classification() {
        // Three classes
        let x_train = vec![
            vec![0.0, 0.0],
            vec![1.0, 0.0],
            vec![5.0, 5.0],
            vec![6.0, 5.0],
            vec![10.0, 10.0],
            vec![11.0, 10.0],
        ];
        let y_train = vec![0, 0, 1, 1, 2, 2];

        let mut knn = KNNClassifier::new(2);
        knn.fit(x_train, y_train);

        let predictions = knn.predict(&vec![
            vec![0.5, 0.0],
            vec![5.5, 5.0],
            vec![10.5, 10.0],
        ]);

        assert_eq!(predictions[0], 0);
        assert_eq!(predictions[1], 1);
        assert_eq!(predictions[2], 2);
    }

    #[test]
    fn test_high_k_smoothing() {
        // With high K, should get more smoothed predictions
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![4.0],
            vec![5.0],
        ];
        let y_train = vec![1.0, 10.0, 3.0, 4.0, 5.0]; // One outlier at x=2

        let mut knn_k1 = KNNRegressor::new(1);
        knn_k1.fit(x_train.clone(), y_train.clone());

        let mut knn_k5 = KNNRegressor::new(5);
        knn_k5.fit(x_train, y_train);

        // Near the outlier
        let pred_k1 = knn_k1.predict_one(&vec![2.1]);
        let pred_k5 = knn_k5.predict_one(&vec![2.1]);

        // K=1 should be close to outlier, K=5 should smooth it out
        assert!(pred_k1 > pred_k5);
    }

    #[test]
    fn test_one_dimensional_classifier() {
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![8.0],
            vec![9.0],
        ];
        let y_train = vec![0, 0, 1, 1];

        let mut knn = KNNClassifier::new(2);
        knn.fit(x_train, y_train);

        assert_eq!(knn.predict_one(&vec![1.5]), 0);
        assert_eq!(knn.predict_one(&vec![8.5]), 1);
    }

    #[test]
    fn test_classification_boundary() {
        // Decision boundary should be around x=5
        let x_train = vec![
            vec![0.0],
            vec![2.0],
            vec![8.0],
            vec![10.0],
        ];
        let y_train = vec![0, 0, 1, 1];

        let mut knn = KNNClassifier::new(2);
        knn.fit(x_train, y_train);

        // Test points on both sides of boundary
        assert_eq!(knn.predict_one(&vec![3.0]), 0);
        assert_eq!(knn.predict_one(&vec![7.0]), 1);
    }
}
