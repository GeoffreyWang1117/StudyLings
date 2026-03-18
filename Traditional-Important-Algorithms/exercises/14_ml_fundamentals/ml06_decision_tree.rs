// ml06_decision_tree.rs
//
// Decision Trees recursively split data based on features to create a tree structure
// for classification or regression. Each internal node tests a feature, each branch
// represents an outcome, and each leaf represents a class label or value.
//
// Key concepts:
// - Entropy: Measure of impurity/disorder in a set: -sum(p_i * log2(p_i))
// - Information Gain: Reduction in entropy after a split
// - Gini Impurity: Alternative to entropy: 1 - sum(p_i^2)
// - CART (Classification and Regression Trees): Uses Gini impurity
// - ID3: Uses information gain (entropy)
// - Stopping criteria: Max depth, min samples, min impurity decrease
//
// Your task: Implement a decision tree classifier using information gain.
//
// Applications:
// - Medical diagnosis
// - Credit risk assessment
// - Customer segmentation
// - Rule extraction

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone)]
pub enum TreeNode {
    Leaf {
        class: usize,
    },
    Internal {
        feature_idx: usize,
        threshold: f64,
        left: Box<TreeNode>,
        right: Box<TreeNode>,
    },
}

pub struct DecisionTreeClassifier {
    root: Option<TreeNode>,
    max_depth: usize,
    min_samples_split: usize,
}

impl DecisionTreeClassifier {
    pub fn new(max_depth: usize, min_samples_split: usize) -> Self {
        Self {
            root: None,
            max_depth,
            min_samples_split,
        }
    }

    fn entropy(y: &[usize]) -> f64 {
        // TODO: Compute entropy: -sum(p_i * log2(p_i))
        // where p_i is proportion of class i
        // 1. Count frequency of each class
        // 2. Compute proportion: p_i = count_i / total
        // 3. Compute entropy: -sum(p_i * log2(p_i))
        // Return 0.0 if all samples are same class (pure)
        // Hint: Use HashMap to count classes
        todo!()
    }

    fn gini_impurity(y: &[usize]) -> f64 {
        // TODO: Compute Gini impurity: 1 - sum(p_i^2)
        // where p_i is proportion of class i
        // 1. Count frequency of each class
        // 2. Compute proportion: p_i = count_i / total
        // 3. Compute Gini: 1 - sum(p_i^2)
        // Return 0.0 if pure (all same class)
        todo!()
    }

    fn information_gain(
        &self,
        x: &[Vec<f64>],
        y: &[usize],
        feature_idx: usize,
        threshold: f64,
    ) -> f64 {
        // TODO: Compute information gain from splitting on feature at threshold
        // 1. Split data into left (x[feature] <= threshold) and right
        // 2. Compute entropy before split: H(parent)
        // 3. Compute weighted entropy after split:
        //    H(children) = (n_left/n_total)*H(left) + (n_right/n_total)*H(right)
        // 4. Information gain = H(parent) - H(children)
        // Higher gain means better split
        todo!()
    }

    fn find_best_split(&self, x: &[Vec<f64>], y: &[usize]) -> Option<(usize, f64)> {
        // TODO: Find the best feature and threshold to split on
        // 1. For each feature:
        //    a. Get unique values (or sample values as candidates)
        //    b. For each value as threshold:
        //       - Compute information gain
        //       - Track best (feature, threshold) with highest gain
        // 2. Return Some((feature_idx, threshold)) or None if no good split
        //
        // Optimization: For continuous features, sort values and try midpoints
        // between consecutive unique values as thresholds
        todo!()
    }

    fn majority_class(y: &[usize]) -> usize {
        // TODO: Return the most frequent class in y
        // Use HashMap to count, return class with max count
        todo!()
    }

    fn split_data(
        &self,
        x: &[Vec<f64>],
        y: &[usize],
        feature_idx: usize,
        threshold: f64,
    ) -> ((Vec<Vec<f64>>, Vec<usize>), (Vec<Vec<f64>>, Vec<usize>)) {
        // TODO: Split data into left and right based on threshold
        // Left: x[feature_idx] <= threshold
        // Right: x[feature_idx] > threshold
        // Return ((x_left, y_left), (x_right, y_right))
        todo!()
    }

    fn build_tree(&self, x: &[Vec<f64>], y: &[usize], depth: usize) -> TreeNode {
        // TODO: Recursively build decision tree
        // Base cases (create Leaf node):
        // 1. All samples have same class (pure)
        // 2. Reached max_depth
        // 3. Too few samples (< min_samples_split)
        // 4. No valid split found
        //
        // Recursive case (create Internal node):
        // 1. Find best split (feature, threshold)
        // 2. Split data into left and right
        // 3. Recursively build left and right subtrees
        // 4. Return Internal node with feature, threshold, and subtrees
        todo!()
    }

    pub fn fit(&mut self, x: &[Vec<f64>], y: &[usize]) {
        // TODO: Build the decision tree
        // Call build_tree starting at depth 0
        // Store result in self.root
        todo!()
    }

    fn predict_one(&self, node: &TreeNode, sample: &[f64]) -> usize {
        // TODO: Traverse tree to make prediction for one sample
        // Match on node type:
        // - Leaf: return class
        // - Internal: compare sample[feature_idx] with threshold
        //   - If <= threshold, recurse left
        //   - If > threshold, recurse right
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>]) -> Vec<usize> {
        // TODO: Predict classes for multiple samples
        // For each sample, call predict_one starting at root
        todo!()
    }

    pub fn accuracy(&self, x: &[Vec<f64>], y: &[usize]) -> f64 {
        // TODO: Compute accuracy
        // (correct predictions) / (total predictions)
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
    fn test_entropy_pure() {
        let y = vec![0, 0, 0, 0];
        let entropy = DecisionTreeClassifier::entropy(&y);
        assert!(approx_eq(entropy, 0.0, 0.001));
    }

    #[test]
    fn test_entropy_balanced() {
        let y = vec![0, 0, 1, 1];
        let entropy = DecisionTreeClassifier::entropy(&y);
        // Maximum entropy for binary: 1.0
        assert!(approx_eq(entropy, 1.0, 0.001));
    }

    #[test]
    fn test_entropy_unbalanced() {
        let y = vec![0, 0, 0, 1];
        let entropy = DecisionTreeClassifier::entropy(&y);
        // Should be between 0 and 1
        assert!(entropy > 0.0 && entropy < 1.0);
    }

    #[test]
    fn test_gini_pure() {
        let y = vec![0, 0, 0, 0];
        let gini = DecisionTreeClassifier::gini_impurity(&y);
        assert!(approx_eq(gini, 0.0, 0.001));
    }

    #[test]
    fn test_gini_balanced() {
        let y = vec![0, 0, 1, 1];
        let gini = DecisionTreeClassifier::gini_impurity(&y);
        // For balanced binary: 1 - (0.5^2 + 0.5^2) = 0.5
        assert!(approx_eq(gini, 0.5, 0.001));
    }

    #[test]
    fn test_majority_class() {
        let y = vec![0, 0, 1, 1, 1];
        let majority = DecisionTreeClassifier::majority_class(&y);
        assert_eq!(majority, 1);
    }

    #[test]
    fn test_simple_tree() {
        // Simple 1D split: x < 5 => class 0, x >= 5 => class 1
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0, 0, 0, 1, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        assert_eq!(predictions, y);
    }

    #[test]
    fn test_2d_classification() {
        // XOR-like pattern (won't be perfectly learned by shallow tree)
        let x = vec![
            vec![0.0, 0.0],
            vec![0.0, 1.0],
            vec![1.0, 0.0],
            vec![1.0, 1.0],
        ];
        let y = vec![0, 1, 1, 0];

        let mut tree = DecisionTreeClassifier::new(3, 1);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        // Should get at least 50% accuracy
        let correct = predictions.iter().zip(y.iter())
            .filter(|(p, a)| p == a)
            .count();
        assert!(correct >= 2);
    }

    #[test]
    fn test_max_depth_1() {
        // With depth 1, can only make one split
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0, 0, 0, 1, 1, 1];

        let mut tree = DecisionTreeClassifier::new(1, 1);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        // Should still get perfect accuracy for this simple problem
        assert_eq!(predictions, y);
    }

    #[test]
    fn test_multiclass() {
        // Three classes
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![5.0],
            vec![6.0],
            vec![9.0],
            vec![10.0],
        ];
        let y = vec![0, 0, 1, 1, 2, 2];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        assert_eq!(predictions, y);
    }

    #[test]
    fn test_min_samples_split() {
        // With min_samples_split=10, won't split a dataset of 4
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0, 0, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 10);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        // Should predict majority class for all
        assert!(predictions.iter().all(|&p| p == predictions[0]));
    }

    #[test]
    fn test_perfect_accuracy() {
        let x = vec![
            vec![1.0, 1.0],
            vec![2.0, 2.0],
            vec![8.0, 8.0],
            vec![9.0, 9.0],
        ];
        let y = vec![0, 0, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x, &y);

        let accuracy = tree.accuracy(&x, &y);
        assert_eq!(accuracy, 1.0);
    }

    #[test]
    fn test_new_data_prediction() {
        let x_train = vec![
            vec![1.0],
            vec![2.0],
            vec![8.0],
            vec![9.0],
        ];
        let y_train = vec![0, 0, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x_train, &y_train);

        let x_test = vec![vec![1.5], vec![8.5]];
        let predictions = tree.predict(&x_test);

        assert_eq!(predictions[0], 0);
        assert_eq!(predictions[1], 1);
    }

    #[test]
    fn test_information_gain() {
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0, 0, 1, 1];

        let tree = DecisionTreeClassifier::new(10, 2);

        // Splitting at 5.0 should give high information gain
        let gain = tree.information_gain(&x, &y, 0, 5.0);
        assert!(gain > 0.5);

        // Splitting at 1.5 should give less information gain
        let bad_gain = tree.information_gain(&x, &y, 0, 1.5);
        assert!(bad_gain < gain);
    }

    #[test]
    fn test_repeated_values() {
        // Dataset with repeated feature values
        let x = vec![
            vec![1.0],
            vec![1.0],
            vec![2.0],
            vec![2.0],
        ];
        let y = vec![0, 0, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        assert_eq!(predictions, y);
    }

    #[test]
    fn test_noisy_data() {
        // Data with some noise
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![4.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
            vec![10.0],
        ];
        let y = vec![0, 0, 0, 1, 1, 1, 1, 0]; // Last one is noise

        let mut tree = DecisionTreeClassifier::new(3, 2);
        tree.fit(&x, &y);

        // Should still get reasonable accuracy
        let accuracy = tree.accuracy(&x, &y);
        assert!(accuracy > 0.6);
    }

    #[test]
    fn test_single_class() {
        // All samples same class
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
        ];
        let y = vec![1, 1, 1];

        let mut tree = DecisionTreeClassifier::new(10, 2);
        tree.fit(&x, &y);

        let predictions = tree.predict(&x);
        assert!(predictions.iter().all(|&p| p == 1));
    }
}
