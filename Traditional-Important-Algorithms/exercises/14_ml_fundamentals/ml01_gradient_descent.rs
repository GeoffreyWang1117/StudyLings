// ml01_gradient_descent.rs
//
// Gradient Descent is a fundamental optimization algorithm used to minimize functions
// by iteratively moving in the direction of steepest descent (negative gradient).
//
// Key concepts:
// - Learning rate: Controls step size (too large = overshoot, too small = slow convergence)
// - SGD (Stochastic Gradient Descent): Uses single sample per iteration
// - Momentum: Accelerates convergence by accumulating velocity
// - Adam: Adaptive learning rates with momentum and RMSprop
//
// Your task: Implement gradient descent variants for optimizing simple functions.
//
// Applications:
// - Training neural networks
// - Linear/logistic regression
// - Any differentiable loss function minimization

// I AM NOT DONE

pub struct GradientDescent {
    learning_rate: f64,
}

impl GradientDescent {
    pub fn new(learning_rate: f64) -> Self {
        Self { learning_rate }
    }

    pub fn optimize<F>(&self, gradient_fn: F, initial: Vec<f64>, iterations: usize) -> Vec<f64>
    where
        F: Fn(&[f64]) -> Vec<f64>,
    {
        // TODO: Implement basic gradient descent
        // 1. Start with initial parameters
        // 2. For each iteration:
        //    a. Compute gradient at current position
        //    b. Update: theta = theta - learning_rate * gradient
        // 3. Return final parameters
        todo!()
    }
}

pub struct MomentumGD {
    learning_rate: f64,
    momentum: f64,
}

impl MomentumGD {
    pub fn new(learning_rate: f64, momentum: f64) -> Self {
        Self { learning_rate, momentum }
    }

    pub fn optimize<F>(&self, gradient_fn: F, initial: Vec<f64>, iterations: usize) -> Vec<f64>
    where
        F: Fn(&[f64]) -> Vec<f64>,
    {
        // TODO: Implement gradient descent with momentum
        // 1. Initialize velocity vector (same size as parameters, all zeros)
        // 2. For each iteration:
        //    a. Compute gradient
        //    b. Update velocity: v = momentum * v - learning_rate * gradient
        //    c. Update parameters: theta = theta + v
        // 3. Return final parameters
        todo!()
    }
}

pub struct Adam {
    learning_rate: f64,
    beta1: f64,  // Exponential decay rate for first moment
    beta2: f64,  // Exponential decay rate for second moment
    epsilon: f64, // Small constant for numerical stability
}

impl Adam {
    pub fn new(learning_rate: f64) -> Self {
        Self {
            learning_rate,
            beta1: 0.9,
            beta2: 0.999,
            epsilon: 1e-8,
        }
    }

    pub fn optimize<F>(&self, gradient_fn: F, initial: Vec<f64>, iterations: usize) -> Vec<f64>
    where
        F: Fn(&[f64]) -> Vec<f64>,
    {
        // TODO: Implement Adam optimizer
        // 1. Initialize first moment (m) and second moment (v) vectors (zeros)
        // 2. For each iteration t:
        //    a. Compute gradient g
        //    b. Update biased first moment: m = beta1 * m + (1 - beta1) * g
        //    c. Update biased second moment: v = beta2 * v + (1 - beta2) * g^2
        //    d. Compute bias-corrected moments:
        //       m_hat = m / (1 - beta1^t)
        //       v_hat = v / (1 - beta2^t)
        //    e. Update parameters: theta = theta - learning_rate * m_hat / (sqrt(v_hat) + epsilon)
        // 3. Return final parameters
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Helper function: f(x) = x^2, gradient = 2x
    fn quadratic_gradient(params: &[f64]) -> Vec<f64> {
        params.iter().map(|x| 2.0 * x).collect()
    }

    // Helper function: f(x, y) = x^2 + y^2, gradient = [2x, 2y]
    fn sphere_gradient(params: &[f64]) -> Vec<f64> {
        params.iter().map(|x| 2.0 * x).collect()
    }

    // Helper function: Rosenbrock function gradient
    // f(x, y) = (1-x)^2 + 100(y-x^2)^2
    fn rosenbrock_gradient(params: &[f64]) -> Vec<f64> {
        let x = params[0];
        let y = params[1];
        vec![
            -2.0 * (1.0 - x) - 400.0 * x * (y - x * x),
            200.0 * (y - x * x),
        ]
    }

    #[test]
    fn test_gradient_descent_simple() {
        let gd = GradientDescent::new(0.1);
        let initial = vec![10.0];
        let result = gd.optimize(quadratic_gradient, initial, 50);

        // Should converge near 0
        assert!(result[0].abs() < 0.1);
    }

    #[test]
    fn test_gradient_descent_2d() {
        let gd = GradientDescent::new(0.1);
        let initial = vec![5.0, 5.0];
        let result = gd.optimize(sphere_gradient, initial, 100);

        // Both parameters should converge near 0
        assert!(result[0].abs() < 0.1);
        assert!(result[1].abs() < 0.1);
    }

    #[test]
    fn test_learning_rate_too_large() {
        let gd = GradientDescent::new(1.5); // Too large
        let initial = vec![1.0];
        let result = gd.optimize(quadratic_gradient, initial, 10);

        // Should diverge or oscillate
        assert!(result[0].abs() > 1.0);
    }

    #[test]
    fn test_momentum_convergence() {
        let momentum = MomentumGD::new(0.01, 0.9);
        let initial = vec![10.0];
        let result = momentum.optimize(quadratic_gradient, initial, 100);

        // Should converge near 0
        assert!(result[0].abs() < 0.1);
    }

    #[test]
    fn test_momentum_faster_than_vanilla() {
        // Momentum should converge faster on sphere function
        let initial = vec![10.0, 10.0];

        let gd = GradientDescent::new(0.01);
        let gd_result = gd.optimize(sphere_gradient, initial.clone(), 50);

        let momentum = MomentumGD::new(0.01, 0.9);
        let momentum_result = momentum.optimize(sphere_gradient, initial, 50);

        // Momentum should be closer to optimum
        let gd_dist = gd_result[0].abs() + gd_result[1].abs();
        let momentum_dist = momentum_result[0].abs() + momentum_result[1].abs();

        assert!(momentum_dist < gd_dist);
    }

    #[test]
    fn test_adam_simple() {
        let adam = Adam::new(0.1);
        let initial = vec![10.0];
        let result = adam.optimize(quadratic_gradient, initial, 50);

        // Should converge near 0
        assert!(result[0].abs() < 0.1);
    }

    #[test]
    fn test_adam_2d() {
        let adam = Adam::new(0.1);
        let initial = vec![5.0, 5.0];
        let result = adam.optimize(sphere_gradient, initial, 100);

        // Both parameters should converge near 0
        assert!(result[0].abs() < 0.1);
        assert!(result[1].abs() < 0.1);
    }

    #[test]
    fn test_adam_rosenbrock() {
        // Rosenbrock function is a challenging optimization problem
        let adam = Adam::new(0.01);
        let initial = vec![0.0, 0.0];
        let result = adam.optimize(rosenbrock_gradient, initial, 1000);

        // Global minimum is at (1, 1)
        // Adam should get reasonably close
        assert!((result[0] - 1.0).abs() < 0.5);
        assert!((result[1] - 1.0).abs() < 0.5);
    }

    #[test]
    fn test_all_optimizers_converge() {
        let initial = vec![8.0, 8.0];

        let gd = GradientDescent::new(0.1);
        let gd_result = gd.optimize(sphere_gradient, initial.clone(), 100);

        let momentum = MomentumGD::new(0.1, 0.9);
        let momentum_result = momentum.optimize(sphere_gradient, initial.clone(), 100);

        let adam = Adam::new(0.1);
        let adam_result = adam.optimize(sphere_gradient, initial, 100);

        // All should converge
        assert!(gd_result[0].abs() < 0.5);
        assert!(momentum_result[0].abs() < 0.5);
        assert!(adam_result[0].abs() < 0.5);
    }

    #[test]
    fn test_zero_learning_rate() {
        let gd = GradientDescent::new(0.0);
        let initial = vec![5.0];
        let result = gd.optimize(quadratic_gradient, initial.clone(), 10);

        // Should not move
        assert_eq!(result[0], initial[0]);
    }

    #[test]
    fn test_adam_beta_parameters() {
        // Test that Adam uses beta1 and beta2 correctly
        let adam = Adam::new(0.1);
        assert_eq!(adam.beta1, 0.9);
        assert_eq!(adam.beta2, 0.999);
        assert_eq!(adam.epsilon, 1e-8);
    }

    #[test]
    fn test_gradient_descent_multiple_params() {
        let gd = GradientDescent::new(0.1);
        let initial = vec![3.0, -4.0, 5.0, -2.0];
        let result = gd.optimize(
            |params| params.iter().map(|x| 2.0 * x).collect(),
            initial,
            100
        );

        // All should converge near 0
        for &val in &result {
            assert!(val.abs() < 0.1);
        }
    }
}
