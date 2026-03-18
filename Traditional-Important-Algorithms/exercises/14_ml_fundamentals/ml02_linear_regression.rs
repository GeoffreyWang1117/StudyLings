// ml02_linear_regression.rs
//
// Linear Regression models the relationship between input features and output
// by fitting a linear equation: y = w0 + w1*x1 + w2*x2 + ... + wn*xn
//
// Key concepts:
// - Normal Equation: Closed-form solution using (X^T X)^-1 X^T y
// - Gradient Descent: Iterative optimization approach
// - Mean Squared Error (MSE): Common loss function
// - Regularization: L2 (Ridge) prevents overfitting
//
// Your task: Implement linear regression with both analytical and iterative methods.
//
// Applications:
// - Price prediction
// - Trend analysis
// - Feature importance analysis

// I AM NOT DONE

pub struct LinearRegression {
    weights: Option<Vec<f64>>,
    bias: f64,
}

impl LinearRegression {
    pub fn new() -> Self {
        Self {
            weights: None,
            bias: 0.0,
        }
    }

    pub fn fit_normal_equation(&mut self, x: &[Vec<f64>], y: &[f64]) {
        // TODO: Implement normal equation solution
        // 1. Add bias column (column of 1s) to X
        // 2. Compute X^T X
        // 3. Compute (X^T X)^-1 using matrix inversion
        // 4. Compute weights: w = (X^T X)^-1 X^T y
        // 5. Extract bias (first weight) and feature weights
        //
        // Hint: For 2x2 matrix inverse:
        // [[a,b],[c,d]]^-1 = 1/(ad-bc) * [[d,-b],[-c,a]]
        // For larger matrices, use Gaussian elimination or iterative methods
        todo!()
    }

    pub fn fit_gradient_descent(
        &mut self,
        x: &[Vec<f64>],
        y: &[f64],
        learning_rate: f64,
        iterations: usize,
    ) {
        // TODO: Implement gradient descent training
        // 1. Initialize weights randomly (small values near 0)
        // 2. For each iteration:
        //    a. Compute predictions: y_pred = X * w + b
        //    b. Compute error: error = y_pred - y
        //    c. Compute gradients:
        //       dw = (1/n) * X^T * error
        //       db = (1/n) * sum(error)
        //    d. Update weights:
        //       w = w - learning_rate * dw
        //       b = b - learning_rate * db
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>]) -> Vec<f64> {
        // TODO: Make predictions for input data
        // For each sample: y = w0*x0 + w1*x1 + ... + wn*xn + bias
        todo!()
    }

    pub fn score(&self, x: &[Vec<f64>], y: &[f64]) -> f64 {
        // TODO: Compute R² score (coefficient of determination)
        // R² = 1 - (SS_res / SS_tot)
        // where SS_res = sum((y - y_pred)^2)
        //       SS_tot = sum((y - y_mean)^2)
        // R² = 1.0 means perfect fit
        // R² = 0.0 means model is as good as predicting the mean
        todo!()
    }

    fn mean_squared_error(&self, x: &[Vec<f64>], y: &[f64]) -> f64 {
        // TODO: Compute MSE = (1/n) * sum((y_pred - y)^2)
        todo!()
    }
}

pub struct RidgeRegression {
    weights: Option<Vec<f64>>,
    bias: f64,
    alpha: f64, // Regularization strength
}

impl RidgeRegression {
    pub fn new(alpha: f64) -> Self {
        Self {
            weights: None,
            bias: 0.0,
            alpha,
        }
    }

    pub fn fit(&mut self, x: &[Vec<f64>], y: &[f64]) {
        // TODO: Implement Ridge regression (L2 regularization)
        // Normal equation with regularization:
        // w = (X^T X + alpha * I)^-1 X^T y
        // where I is identity matrix, alpha is regularization strength
        // This penalizes large weights, preventing overfitting
        todo!()
    }

    pub fn predict(&self, x: &[Vec<f64>]) -> Vec<f64> {
        // TODO: Same as LinearRegression prediction
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
    fn test_perfect_linear_fit() {
        // y = 2x + 3
        let x = vec![vec![1.0], vec![2.0], vec![3.0], vec![4.0]];
        let y = vec![5.0, 7.0, 9.0, 11.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let predictions = model.predict(&x);
        for (pred, actual) in predictions.iter().zip(y.iter()) {
            assert!(approx_eq(*pred, *actual, 0.01));
        }
    }

    #[test]
    fn test_gradient_descent_simple() {
        // y = 2x + 3
        let x = vec![vec![1.0], vec![2.0], vec![3.0], vec![4.0]];
        let y = vec![5.0, 7.0, 9.0, 11.0];

        let mut model = LinearRegression::new();
        model.fit_gradient_descent(&x, &y, 0.01, 1000);

        let predictions = model.predict(&x);
        for (pred, actual) in predictions.iter().zip(y.iter()) {
            assert!(approx_eq(*pred, *actual, 0.1));
        }
    }

    #[test]
    fn test_multiple_features() {
        // y = 2*x1 + 3*x2 + 1
        let x = vec![
            vec![1.0, 1.0],
            vec![2.0, 2.0],
            vec![3.0, 3.0],
            vec![4.0, 4.0],
        ];
        let y = vec![6.0, 11.0, 16.0, 21.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let predictions = model.predict(&x);
        for (pred, actual) in predictions.iter().zip(y.iter()) {
            assert!(approx_eq(*pred, *actual, 0.01));
        }
    }

    #[test]
    fn test_r_squared_perfect_fit() {
        let x = vec![vec![1.0], vec![2.0], vec![3.0], vec![4.0]];
        let y = vec![5.0, 7.0, 9.0, 11.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let r2 = model.score(&x, &y);
        assert!(approx_eq(r2, 1.0, 0.01));
    }

    #[test]
    fn test_r_squared_imperfect_fit() {
        let x = vec![vec![1.0], vec![2.0], vec![3.0], vec![4.0]];
        let y = vec![5.0, 7.5, 9.0, 11.2]; // Slight noise

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let r2 = model.score(&x, &y);
        assert!(r2 > 0.95); // Should still be very high
        assert!(r2 < 1.0);
    }

    #[test]
    fn test_mse_calculation() {
        let x = vec![vec![1.0], vec![2.0], vec![3.0]];
        let y = vec![2.0, 4.0, 6.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let mse = model.mean_squared_error(&x, &y);
        assert!(mse < 0.01); // Should be very small for good fit
    }

    #[test]
    fn test_prediction_new_data() {
        // Train on y = 2x + 3
        let x_train = vec![vec![1.0], vec![2.0], vec![3.0]];
        let y_train = vec![5.0, 7.0, 9.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x_train, &y_train);

        // Predict on new data
        let x_test = vec![vec![5.0], vec![6.0]];
        let predictions = model.predict(&x_test);

        assert!(approx_eq(predictions[0], 13.0, 0.01));
        assert!(approx_eq(predictions[1], 15.0, 0.01));
    }

    #[test]
    fn test_ridge_regression_basic() {
        let x = vec![vec![1.0], vec![2.0], vec![3.0], vec![4.0]];
        let y = vec![5.0, 7.0, 9.0, 11.0];

        let mut model = RidgeRegression::new(0.1);
        model.fit(&x, &y);

        let predictions = model.predict(&x);
        // With regularization, fit might not be perfect but should be close
        for (pred, actual) in predictions.iter().zip(y.iter()) {
            assert!((pred - actual).abs() < 0.5);
        }
    }

    #[test]
    fn test_ridge_vs_linear() {
        // Ridge should produce smaller weights with regularization
        let x = vec![
            vec![1.0, 2.0],
            vec![2.0, 4.0],
            vec![3.0, 6.0],
            vec![4.0, 8.0],
        ];
        let y = vec![5.0, 9.0, 13.0, 17.0];

        let mut linear = LinearRegression::new();
        linear.fit_normal_equation(&x, &y);

        let mut ridge = RidgeRegression::new(10.0); // Strong regularization
        ridge.fit(&x, &y);

        // Ridge weights should be smaller in magnitude
        let linear_weights = linear.weights.unwrap();
        let ridge_weights = ridge.weights.unwrap();

        let linear_norm: f64 = linear_weights.iter().map(|w| w * w).sum::<f64>().sqrt();
        let ridge_norm: f64 = ridge_weights.iter().map(|w| w * w).sum::<f64>().sqrt();

        assert!(ridge_norm < linear_norm);
    }

    #[test]
    fn test_batch_predictions() {
        let x_train = vec![vec![1.0], vec![2.0], vec![3.0]];
        let y_train = vec![3.0, 5.0, 7.0]; // y = 2x + 1

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x_train, &y_train);

        let x_test = vec![vec![4.0], vec![5.0], vec![6.0]];
        let predictions = model.predict(&x_test);

        assert_eq!(predictions.len(), 3);
        assert!(approx_eq(predictions[0], 9.0, 0.01));
        assert!(approx_eq(predictions[1], 11.0, 0.01));
        assert!(approx_eq(predictions[2], 13.0, 0.01));
    }

    #[test]
    fn test_gradient_descent_convergence() {
        let x = vec![
            vec![1.0, 2.0],
            vec![2.0, 3.0],
            vec![3.0, 4.0],
            vec![4.0, 5.0],
        ];
        let y = vec![8.0, 13.0, 18.0, 23.0];

        let mut model = LinearRegression::new();
        model.fit_gradient_descent(&x, &y, 0.01, 5000);

        let r2 = model.score(&x, &y);
        assert!(r2 > 0.95); // Should achieve good fit
    }

    #[test]
    fn test_zero_input() {
        // Test with zero features
        let x = vec![vec![0.0], vec![0.0], vec![0.0]];
        let y = vec![5.0, 5.0, 5.0];

        let mut model = LinearRegression::new();
        model.fit_normal_equation(&x, &y);

        let predictions = model.predict(&x);
        // Should predict approximately the mean (bias term)
        for pred in predictions.iter() {
            assert!(approx_eq(*pred, 5.0, 0.1));
        }
    }
}
