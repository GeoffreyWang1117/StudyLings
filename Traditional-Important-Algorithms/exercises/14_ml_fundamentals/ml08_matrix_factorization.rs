// ml08_matrix_factorization.rs
//
// Matrix Factorization decomposes a matrix into the product of two or more matrices
// to discover latent features. Widely used in recommender systems and dimensionality reduction.
//
// Key concepts:
// - SVD (Singular Value Decomposition): A = U Σ V^T, exact factorization
// - NMF (Non-negative Matrix Factorization): A ≈ W H, all values ≥ 0
// - Latent factors: Hidden features learned from data
// - Collaborative filtering: Predict missing values (e.g., movie ratings)
// - Regularization: Prevents overfitting by penalizing large values
//
// Your task: Implement matrix factorization for recommendation systems.
//
// Applications:
// - Movie/product recommendations (Netflix Prize)
// - Topic modeling (documents = topics × words)
// - Image compression
// - Audio source separation

// I AM NOT DONE

use std::collections::HashMap;

pub struct MatrixFactorization {
    num_users: usize,
    num_items: usize,
    num_factors: usize,
    user_factors: Vec<Vec<f64>>,
    item_factors: Vec<Vec<f64>>,
    learning_rate: f64,
    regularization: f64,
}

impl MatrixFactorization {
    pub fn new(
        num_users: usize,
        num_items: usize,
        num_factors: usize,
        learning_rate: f64,
        regularization: f64,
    ) -> Self {
        // TODO: Initialize matrix factorization model
        // 1. Create user_factors: num_users × num_factors matrix
        // 2. Create item_factors: num_items × num_factors matrix
        // 3. Initialize both with small random values (e.g., 0.0 to 0.1)
        //    Random initialization helps break symmetry
        // For testing, you can use simple sequential values
        todo!()
    }

    pub fn predict(&self, user_id: usize, item_id: usize) -> f64 {
        // TODO: Predict rating for user-item pair
        // Prediction = dot product of user_factors[user_id] and item_factors[item_id]
        // rating ≈ sum(user_factors[user_id][k] * item_factors[item_id][k] for all k)
        todo!()
    }

    pub fn train_one(
        &mut self,
        user_id: usize,
        item_id: usize,
        rating: f64,
    ) {
        // TODO: Update factors for one user-item-rating triple using SGD
        // 1. Compute prediction: pred = dot(user_factors[user], item_factors[item])
        // 2. Compute error: error = rating - pred
        // 3. Update factors with gradient descent:
        //    For each latent factor k:
        //      user_factors[user][k] += learning_rate * (error * item_factors[item][k] - regularization * user_factors[user][k])
        //      item_factors[item][k] += learning_rate * (error * user_factors[user][k] - regularization * item_factors[item][k])
        //
        // Regularization term prevents overfitting by penalizing large values
        todo!()
    }

    pub fn train(
        &mut self,
        ratings: &[(usize, usize, f64)], // (user_id, item_id, rating)
        epochs: usize,
    ) {
        // TODO: Train on all ratings for multiple epochs
        // For each epoch:
        //   For each (user_id, item_id, rating) in ratings:
        //     Call train_one
        // Optionally: Shuffle ratings each epoch for better convergence
        todo!()
    }

    pub fn rmse(&self, ratings: &[(usize, usize, f64)]) -> f64 {
        // TODO: Compute Root Mean Squared Error
        // RMSE = sqrt((1/n) * sum((predicted - actual)^2))
        // Measures prediction accuracy on known ratings
        todo!()
    }

    pub fn get_user_factors(&self, user_id: usize) -> &[f64] {
        // TODO: Return latent factors for a user
        &self.user_factors[user_id]
    }

    pub fn get_item_factors(&self, item_id: usize) -> &[f64] {
        // TODO: Return latent factors for an item
        &self.item_factors[item_id]
    }

    pub fn recommend_items(&self, user_id: usize, top_n: usize) -> Vec<(usize, f64)> {
        // TODO: Recommend top N items for a user
        // 1. Predict ratings for all items
        // 2. Sort by predicted rating (descending)
        // 3. Return top N as (item_id, predicted_rating) pairs
        todo!()
    }
}

pub struct NMF {
    num_samples: usize,
    num_features: usize,
    num_components: usize,
    w: Vec<Vec<f64>>, // num_samples × num_components
    h: Vec<Vec<f64>>, // num_components × num_features
}

impl NMF {
    pub fn new(num_samples: usize, num_features: usize, num_components: usize) -> Self {
        // TODO: Initialize NMF
        // 1. Create W matrix: num_samples × num_components
        // 2. Create H matrix: num_components × num_features
        // 3. Initialize with small positive random values
        // All values must remain non-negative throughout
        todo!()
    }

    pub fn fit(&mut self, data: &[Vec<f64>], iterations: usize) {
        // TODO: Fit NMF using multiplicative update rules
        // Goal: Find W and H such that data ≈ W × H
        // All matrices must remain non-negative
        //
        // Update rules (multiplicative):
        // H = H * (W^T × data) / (W^T × W × H + epsilon)
        // W = W * (data × H^T) / (W × H × H^T + epsilon)
        //
        // Where:
        // - * is element-wise multiplication
        // - / is element-wise division
        // - × is matrix multiplication
        // - epsilon (e.g., 1e-10) prevents division by zero
        //
        // Repeat for specified iterations
        todo!()
    }

    pub fn transform(&self, data: &[Vec<f64>]) -> Vec<Vec<f64>> {
        // TODO: Transform new data using learned H
        // Given data and H, find W such that data ≈ W × H
        // Return W (representation in latent space)
        todo!()
    }

    pub fn reconstruct(&self) -> Vec<Vec<f64>> {
        // TODO: Reconstruct original matrix
        // Return W × H
        todo!()
    }

    pub fn reconstruction_error(&self, data: &[Vec<f64>]) -> f64 {
        // TODO: Compute reconstruction error
        // Frobenius norm: sqrt(sum((data[i][j] - (W×H)[i][j])^2))
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
    fn test_matrix_factorization_creation() {
        let mf = MatrixFactorization::new(10, 20, 5, 0.01, 0.02);

        assert_eq!(mf.num_users, 10);
        assert_eq!(mf.num_items, 20);
        assert_eq!(mf.num_factors, 5);
        assert_eq!(mf.user_factors.len(), 10);
        assert_eq!(mf.item_factors.len(), 20);
    }

    #[test]
    fn test_simple_prediction() {
        let mf = MatrixFactorization::new(2, 2, 2, 0.01, 0.0);

        // Should be able to predict (value depends on initialization)
        let pred = mf.predict(0, 0);
        assert!(pred >= 0.0);
    }

    #[test]
    fn test_perfect_factorization() {
        // Simple 2×2 matrix with rank 1
        // [1, 2]   [1]
        // [2, 4] = [2] × [1, 2]
        //
        // User 0 rates item 0: 1, item 1: 2
        // User 1 rates item 0: 2, item 1: 4
        let ratings = vec![
            (0, 0, 1.0),
            (0, 1, 2.0),
            (1, 0, 2.0),
            (1, 1, 4.0),
        ];

        let mut mf = MatrixFactorization::new(2, 2, 1, 0.1, 0.0);
        mf.train(&ratings, 1000);

        // Should predict accurately
        for &(user, item, rating) in &ratings {
            let pred = mf.predict(user, item);
            assert!((pred - rating).abs() < 0.5);
        }
    }

    #[test]
    fn test_rmse_decreases() {
        let ratings = vec![
            (0, 0, 5.0),
            (0, 1, 3.0),
            (1, 0, 4.0),
            (1, 1, 2.0),
        ];

        let mut mf = MatrixFactorization::new(2, 2, 2, 0.1, 0.01);

        let rmse_before = mf.rmse(&ratings);
        mf.train(&ratings, 100);
        let rmse_after = mf.rmse(&ratings);

        // RMSE should decrease with training
        assert!(rmse_after < rmse_before);
    }

    #[test]
    fn test_regularization_effect() {
        let ratings = vec![
            (0, 0, 5.0),
            (0, 1, 1.0),
        ];

        // No regularization
        let mut mf_no_reg = MatrixFactorization::new(1, 2, 2, 0.1, 0.0);
        mf_no_reg.train(&ratings, 500);

        // Strong regularization
        let mut mf_reg = MatrixFactorization::new(1, 2, 2, 0.1, 0.5);
        mf_reg.train(&ratings, 500);

        // Regularized model should have smaller factor magnitudes
        let factors_no_reg: f64 = mf_no_reg.user_factors[0].iter().map(|x| x * x).sum();
        let factors_reg: f64 = mf_reg.user_factors[0].iter().map(|x| x * x).sum();

        assert!(factors_reg < factors_no_reg);
    }

    #[test]
    fn test_recommendation() {
        let ratings = vec![
            (0, 0, 5.0),
            (0, 1, 3.0),
            (0, 2, 1.0),
        ];

        let mut mf = MatrixFactorization::new(1, 3, 2, 0.1, 0.01);
        mf.train(&ratings, 500);

        let recommendations = mf.recommend_items(0, 2);

        // Should recommend top 2 items
        assert_eq!(recommendations.len(), 2);

        // Items should be sorted by predicted rating
        assert!(recommendations[0].1 >= recommendations[1].1);
    }

    #[test]
    fn test_cold_start_user() {
        // New user (id=2) not in training data
        let ratings = vec![
            (0, 0, 5.0),
            (1, 0, 4.0),
        ];

        let mf = MatrixFactorization::new(3, 1, 2, 0.1, 0.01);

        // Should still be able to make prediction (based on initialization)
        let pred = mf.predict(2, 0);
        assert!(pred >= 0.0);
    }

    #[test]
    fn test_sparse_ratings() {
        // Sparse rating matrix (most entries unknown)
        let ratings = vec![
            (0, 0, 5.0),
            (1, 2, 3.0),
            (2, 1, 4.0),
        ];

        let mut mf = MatrixFactorization::new(3, 3, 2, 0.1, 0.01);
        mf.train(&ratings, 100);

        // Can predict for all user-item pairs
        for user in 0..3 {
            for item in 0..3 {
                let pred = mf.predict(user, item);
                assert!(pred.is_finite());
            }
        }
    }

    #[test]
    fn test_nmf_creation() {
        let nmf = NMF::new(10, 20, 5);

        assert_eq!(nmf.num_samples, 10);
        assert_eq!(nmf.num_features, 20);
        assert_eq!(nmf.num_components, 5);
        assert_eq!(nmf.w.len(), 10);
        assert_eq!(nmf.h.len(), 5);
    }

    #[test]
    fn test_nmf_simple_factorization() {
        // Simple non-negative matrix
        let data = vec![
            vec![2.0, 4.0],
            vec![1.0, 2.0],
        ];

        let mut nmf = NMF::new(2, 2, 1);
        nmf.fit(&data, 100);

        let error = nmf.reconstruction_error(&data);
        // Should achieve low reconstruction error
        assert!(error < 1.0);
    }

    #[test]
    fn test_nmf_non_negativity() {
        let data = vec![
            vec![1.0, 2.0, 3.0],
            vec![4.0, 5.0, 6.0],
        ];

        let mut nmf = NMF::new(2, 3, 2);
        nmf.fit(&data, 50);

        // All factors should be non-negative
        for row in &nmf.w {
            for &val in row {
                assert!(val >= 0.0);
            }
        }

        for row in &nmf.h {
            for &val in row {
                assert!(val >= 0.0);
            }
        }
    }

    #[test]
    fn test_nmf_reconstruction() {
        let data = vec![
            vec![1.0, 2.0],
            vec![3.0, 4.0],
        ];

        let mut nmf = NMF::new(2, 2, 2);
        nmf.fit(&data, 200);

        let reconstructed = nmf.reconstruct();

        // Reconstructed should be close to original
        for i in 0..2 {
            for j in 0..2 {
                assert!((reconstructed[i][j] - data[i][j]).abs() < 1.0);
            }
        }
    }

    #[test]
    fn test_nmf_error_decreases() {
        let data = vec![
            vec![2.0, 3.0, 4.0],
            vec![1.0, 2.0, 3.0],
            vec![3.0, 4.0, 5.0],
        ];

        let mut nmf = NMF::new(3, 3, 2);

        let error_before = nmf.reconstruction_error(&data);
        nmf.fit(&data, 100);
        let error_after = nmf.reconstruction_error(&data);

        // Error should decrease
        assert!(error_after < error_before);
    }

    #[test]
    fn test_latent_factors_dimension() {
        let mf = MatrixFactorization::new(5, 10, 3, 0.01, 0.01);

        let user_factors = mf.get_user_factors(0);
        let item_factors = mf.get_item_factors(0);

        assert_eq!(user_factors.len(), 3);
        assert_eq!(item_factors.len(), 3);
    }

    #[test]
    fn test_collaborative_filtering() {
        // User 0 and User 1 have similar taste
        // User 0: likes item 0 (5), dislikes item 1 (1)
        // User 1: likes item 0 (5), unknown for item 1
        // Should predict User 1 dislikes item 1 too
        let ratings = vec![
            (0, 0, 5.0),
            (0, 1, 1.0),
            (1, 0, 5.0),
            (0, 2, 3.0),
            (1, 2, 3.0),
        ];

        let mut mf = MatrixFactorization::new(2, 3, 2, 0.1, 0.01);
        mf.train(&ratings, 500);

        let pred = mf.predict(1, 1);
        // Should predict low rating (< 3)
        assert!(pred < 3.0);
    }
}
