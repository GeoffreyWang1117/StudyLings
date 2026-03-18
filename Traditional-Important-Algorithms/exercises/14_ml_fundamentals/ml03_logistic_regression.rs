// ml03_logistic_regression.rs
//
// Logistic Regression is used for binary classification by modeling the probability
// that an instance belongs to a particular class using the logistic (sigmoid) function.
//
// Key concepts:
// - Sigmoid function: σ(z) = 1 / (1 + e^(-z)), outputs probability in [0, 1]
// - Log loss (Binary Cross-Entropy): -[y*log(p) + (1-y)*log(1-p)]
// - Decision boundary: Threshold (typically 0.5) to classify predictions
// - Gradient descent: Used for optimization since no closed-form solution
//
// Your task: Implement logistic regression for binary classification.
//
// Applications:
// - Spam detection
// - Disease diagnosis
// - Customer churn prediction
// - Credit risk assessment

// I AM NOT DONE

pub struct LogisticRegression {
    weights: Option<Vec<f64>>,
    bias: f64,
}

impl LogisticRegression {
    pub fn new() -> Self {
        Self {
            weights: None,
            bias: 0.0,
        }
    }

    fn sigmoid(z: f64) -> f64 {
        // TODO: Implement sigmoid function: 1 / (1 + e^(-z))
        // This maps any real number to range (0, 1)
        // Handle overflow: if z is very negative, e^(-z) can overflow
        // Hint: For z < 0, use σ(z) = e^z / (1 + e^z) for numerical stability
        todo!()
    }

    fn sigmoid_derivative(z: f64) -> f64 {
        // TODO: Implement sigmoid derivative: σ(z) * (1 - σ(z))
        // This is used in gradient computation
        todo!()
    }

    pub fn fit(&mut self, x: &[Vec<f64>], y: &[f64], learning_rate: f64, iterations: usize) {
        // TODO: Train using gradient descent
        // 1. Initialize weights to small random values
        // 2. For each iteration:
        //    a. Compute predictions: z = X*w + b, then p = sigmoid(z)
        //    b. Compute gradients:
        //       dw = (1/n) * X^T * (p - y)
        //       db = (1/n) * sum(p - y)
        //    c. Update weights:
        //       w = w - learning_rate * dw
        //       b = b - learning_rate * db
        todo!()
    }

    pub fn predict_proba(&self, x: &[Vec<f64>]) -> Vec<f64> {
        // TODO: Predict probabilities for each sample
        // For each sample: z = w^T * x + b, then p = sigmoid(z)
        // Returns probabilities in range [0, 1]
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>], threshold: f64) -> Vec<u8> {
        // TODO: Predict class labels (0 or 1)
        // Use threshold (typically 0.5) to convert probabilities to binary labels
        // If probability >= threshold, predict 1, else predict 0
        todo!()
    }

    pub fn accuracy(&self, x: &[Vec<f64>], y: &[f64]) -> f64 {
        // TODO: Compute classification accuracy
        // accuracy = (number of correct predictions) / (total predictions)
        todo!()
    }

    fn log_loss(&self, x: &[Vec<f64>], y: &[f64]) -> f64 {
        // TODO: Compute binary cross-entropy loss
        // loss = -(1/n) * sum[y*log(p) + (1-y)*log(1-p)]
        // where p is predicted probability
        // Add small epsilon (1e-15) to avoid log(0)
        todo!()
    }

    pub fn precision_recall(&self, x: &[Vec<f64>], y: &[f64], threshold: f64) -> (f64, f64) {
        // TODO: Compute precision and recall
        // precision = TP / (TP + FP)
        // recall = TP / (TP + FN)
        // where TP = true positives, FP = false positives, FN = false negatives
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
    fn test_sigmoid_basic() {
        assert!(approx_eq(LogisticRegression::sigmoid(0.0), 0.5, 0.001));
        assert!(LogisticRegression::sigmoid(5.0) > 0.99);
        assert!(LogisticRegression::sigmoid(-5.0) < 0.01);
    }

    #[test]
    fn test_sigmoid_bounds() {
        // Sigmoid should always be in (0, 1)
        for z in [-100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0] {
            let s = LogisticRegression::sigmoid(z);
            assert!(s > 0.0 && s < 1.0);
        }
    }

    #[test]
    fn test_sigmoid_derivative() {
        // At z=0, derivative should be 0.25
        assert!(approx_eq(LogisticRegression::sigmoid_derivative(0.0), 0.25, 0.001));
    }

    #[test]
    fn test_linearly_separable() {
        // Simple linearly separable data: x > 5 => class 1
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![4.0],
            vec![6.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        let accuracy = model.accuracy(&x, &y);
        assert!(accuracy > 0.9); // Should achieve high accuracy
    }

    #[test]
    fn test_predict_proba_range() {
        let x = vec![vec![1.0], vec![2.0], vec![3.0]];
        let y = vec![0.0, 0.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 100);

        let probas = model.predict_proba(&x);

        // All probabilities should be in [0, 1]
        for p in probas {
            assert!(p >= 0.0 && p <= 1.0);
        }
    }

    #[test]
    fn test_predict_binary() {
        let x = vec![vec![1.0], vec![2.0], vec![8.0], vec![9.0]];
        let y = vec![0.0, 0.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        let predictions = model.predict(&x, 0.5);

        // Predictions should be 0 or 1
        for &pred in &predictions {
            assert!(pred == 0 || pred == 1);
        }
    }

    #[test]
    fn test_two_features() {
        // XOR-like problem (not perfectly linearly separable, but close)
        let x = vec![
            vec![0.0, 0.0],
            vec![0.0, 1.0],
            vec![1.0, 0.0],
            vec![1.0, 1.0],
            vec![0.1, 0.1],
            vec![0.9, 0.9],
        ];
        let y = vec![0.0, 1.0, 1.0, 0.0, 0.0, 0.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        // Won't get perfect accuracy (XOR isn't linearly separable)
        // but should learn something
        let accuracy = model.accuracy(&x, &y);
        assert!(accuracy > 0.4);
    }

    #[test]
    fn test_log_loss_decreases() {
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0.0, 0.0, 0.0, 1.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();

        // Train for a few iterations
        model.fit(&x, &y, 0.1, 10);
        let loss_early = model.log_loss(&x, &y);

        // Continue training
        model.fit(&x, &y, 0.1, 100);
        let loss_late = model.log_loss(&x, &y);

        // Loss should decrease with more training
        assert!(loss_late < loss_early);
    }

    #[test]
    fn test_precision_recall() {
        let x = vec![
            vec![1.0],
            vec![2.0],
            vec![3.0],
            vec![7.0],
            vec![8.0],
            vec![9.0],
        ];
        let y = vec![0.0, 0.0, 0.0, 1.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        let (precision, recall) = model.precision_recall(&x, &y, 0.5);

        // Both should be reasonably high for this simple problem
        assert!(precision > 0.7);
        assert!(recall > 0.7);
    }

    #[test]
    fn test_threshold_effect() {
        let x = vec![vec![1.0], vec![5.0], vec![9.0]];
        let y = vec![0.0, 0.5, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 500);

        let pred_low = model.predict(&x, 0.3);
        let pred_high = model.predict(&x, 0.7);

        // Lower threshold should predict more 1s
        let sum_low: u8 = pred_low.iter().sum();
        let sum_high: u8 = pred_high.iter().sum();

        assert!(sum_low >= sum_high);
    }

    #[test]
    fn test_perfect_separation() {
        // Perfectly separable: all negative x < 0, all positive x > 0
        let x = vec![
            vec![-5.0],
            vec![-3.0],
            vec![-1.0],
            vec![1.0],
            vec![3.0],
            vec![5.0],
        ];
        let y = vec![0.0, 0.0, 0.0, 1.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 2000);

        let accuracy = model.accuracy(&x, &y);
        assert!(accuracy >= 0.95); // Should achieve near-perfect accuracy
    }

    #[test]
    fn test_balanced_dataset() {
        // Equal number of positive and negative examples
        let x = vec![
            vec![1.0, 1.0],
            vec![2.0, 2.0],
            vec![8.0, 8.0],
            vec![9.0, 9.0],
        ];
        let y = vec![0.0, 0.0, 1.0, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        let (precision, recall) = model.precision_recall(&x, &y, 0.5);

        // For balanced data, precision and recall should be similar
        assert!((precision - recall).abs() < 0.3);
    }

    #[test]
    fn test_confidence_scores() {
        let x = vec![
            vec![0.0],
            vec![5.0],
            vec![10.0],
        ];
        let y = vec![0.0, 0.5, 1.0];

        let mut model = LogisticRegression::new();
        model.fit(&x, &y, 0.1, 1000);

        let probas = model.predict_proba(&x);

        // Probabilities should increase with x
        assert!(probas[0] < probas[1]);
        assert!(probas[1] < probas[2]);
    }
}
