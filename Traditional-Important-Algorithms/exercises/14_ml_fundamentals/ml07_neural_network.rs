// ml07_neural_network.rs
//
// A Neural Network is a computational model inspired by biological neurons, consisting
// of layers of interconnected nodes that transform inputs through weighted connections.
//
// Key concepts:
// - Forward propagation: Compute output by passing input through layers
// - Activation functions: Non-linear transformations (sigmoid, ReLU, tanh)
// - Backpropagation: Compute gradients using chain rule, propagate errors backward
// - Weight update: Adjust weights using gradient descent
// - Loss function: Measures prediction error (MSE, cross-entropy)
//
// Your task: Implement a simple feedforward neural network with backpropagation.
//
// Architecture: Input -> Hidden Layer -> Output Layer
//
// Applications:
// - Image recognition
// - Natural language processing
// - Time series prediction
// - Function approximation

// I AM NOT DONE

pub struct NeuralNetwork {
    // Weights: input -> hidden
    weights_ih: Vec<Vec<f64>>,
    bias_h: Vec<f64>,

    // Weights: hidden -> output
    weights_ho: Vec<Vec<f64>>,
    bias_o: Vec<f64>,

    learning_rate: f64,
}

impl NeuralNetwork {
    pub fn new(input_size: usize, hidden_size: usize, output_size: usize, learning_rate: f64) -> Self {
        // TODO: Initialize network with random small weights
        // 1. Create weights_ih: hidden_size x input_size matrix
        // 2. Create bias_h: hidden_size vector
        // 3. Create weights_ho: output_size x hidden_size matrix
        // 4. Create bias_o: output_size vector
        // Initialize weights to small random values (e.g., -0.5 to 0.5)
        // Initialize biases to 0.0
        // Hint: Use nested Vec for matrices
        todo!()
    }

    fn sigmoid(x: f64) -> f64 {
        // TODO: Implement sigmoid: 1 / (1 + e^(-x))
        // Handle numerical stability for large negative x
        todo!()
    }

    fn sigmoid_derivative(x: f64) -> f64 {
        // TODO: Implement sigmoid derivative: sigmoid(x) * (1 - sigmoid(x))
        // Can also be computed as: x * (1 - x) where x is already sigmoid output
        todo!()
    }

    fn relu(x: f64) -> f64 {
        // TODO: Implement ReLU: max(0, x)
        todo!()
    }

    fn relu_derivative(x: f64) -> f64 {
        // TODO: Implement ReLU derivative: 1 if x > 0, else 0
        todo!()
    }

    fn tanh(x: f64) -> f64 {
        // TODO: Implement tanh: (e^x - e^(-x)) / (e^x + e^(-x))
        // Or use x.tanh()
        todo!()
    }

    fn tanh_derivative(x: f64) -> f64 {
        // TODO: Implement tanh derivative: 1 - tanh(x)^2
        todo!()
    }

    fn forward(&self, input: &[f64]) -> (Vec<f64>, Vec<f64>) {
        // TODO: Forward propagation
        // 1. Compute hidden layer activations:
        //    hidden_input = weights_ih * input + bias_h
        //    hidden_output = sigmoid(hidden_input)
        // 2. Compute output layer activations:
        //    output_input = weights_ho * hidden_output + bias_o
        //    output_output = sigmoid(output_input)
        // 3. Return (hidden_output, output_output)
        //
        // Matrix multiplication: result[i] = sum(weights[i][j] * input[j]) + bias[i]
        todo!()
    }

    pub fn predict(&self, input: &[f64]) -> Vec<f64> {
        // TODO: Make prediction without training
        // Run forward propagation and return output
        todo!()
    }

    pub fn train_one(&mut self, input: &[f64], target: &[f64]) {
        // TODO: Train on one sample using backpropagation
        //
        // 1. Forward pass:
        //    - Compute hidden and output activations
        //
        // 2. Compute output layer error:
        //    output_error = target - output
        //    output_delta = output_error * sigmoid_derivative(output)
        //
        // 3. Compute hidden layer error:
        //    hidden_error = weights_ho^T * output_delta
        //    hidden_delta = hidden_error * sigmoid_derivative(hidden)
        //
        // 4. Update weights and biases:
        //    weights_ho += learning_rate * output_delta * hidden^T
        //    bias_o += learning_rate * output_delta
        //    weights_ih += learning_rate * hidden_delta * input^T
        //    bias_h += learning_rate * hidden_delta
        todo!()
    }

    pub fn train(&mut self, inputs: &[Vec<f64>], targets: &[Vec<f64>], epochs: usize) {
        // TODO: Train on dataset for multiple epochs
        // For each epoch:
        //   For each (input, target) pair:
        //     Call train_one
        todo!()
    }

    pub fn mean_squared_error(&self, inputs: &[Vec<f64>], targets: &[Vec<f64>]) -> f64 {
        // TODO: Compute MSE across all samples
        // MSE = (1/n) * sum over samples( sum over outputs( (predicted - actual)^2 ) )
        todo!()
    }

    pub fn accuracy(&self, inputs: &[Vec<f64>], targets: &[Vec<f64>]) -> f64 {
        // TODO: Compute classification accuracy
        // For each sample:
        //   - Predict (get output vector)
        //   - Find index of max value in prediction
        //   - Find index of max value in target (one-hot encoded)
        //   - Compare indices
        // Return percentage of correct predictions
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
    fn test_sigmoid() {
        assert!(approx_eq(NeuralNetwork::sigmoid(0.0), 0.5, 0.001));
        assert!(NeuralNetwork::sigmoid(5.0) > 0.99);
        assert!(NeuralNetwork::sigmoid(-5.0) < 0.01);
    }

    #[test]
    fn test_sigmoid_derivative() {
        // At sigmoid(0) = 0.5, derivative should be 0.25
        let s = NeuralNetwork::sigmoid(0.0);
        let ds = NeuralNetwork::sigmoid_derivative(s);
        assert!(approx_eq(ds, 0.25, 0.001));
    }

    #[test]
    fn test_relu() {
        assert_eq!(NeuralNetwork::relu(-1.0), 0.0);
        assert_eq!(NeuralNetwork::relu(0.0), 0.0);
        assert_eq!(NeuralNetwork::relu(5.0), 5.0);
    }

    #[test]
    fn test_relu_derivative() {
        assert_eq!(NeuralNetwork::relu_derivative(-1.0), 0.0);
        assert_eq!(NeuralNetwork::relu_derivative(0.0), 0.0);
        assert_eq!(NeuralNetwork::relu_derivative(5.0), 1.0);
    }

    #[test]
    fn test_tanh() {
        assert!(approx_eq(NeuralNetwork::tanh(0.0), 0.0, 0.001));
        assert!(NeuralNetwork::tanh(5.0) > 0.99);
        assert!(NeuralNetwork::tanh(-5.0) < -0.99);
    }

    #[test]
    fn test_network_creation() {
        let nn = NeuralNetwork::new(2, 3, 1, 0.1);

        // Check dimensions
        assert_eq!(nn.weights_ih.len(), 3); // hidden_size
        assert_eq!(nn.weights_ih[0].len(), 2); // input_size
        assert_eq!(nn.weights_ho.len(), 1); // output_size
        assert_eq!(nn.weights_ho[0].len(), 3); // hidden_size
    }

    #[test]
    fn test_forward_propagation() {
        let nn = NeuralNetwork::new(2, 2, 1, 0.1);
        let input = vec![0.5, 0.5];
        let output = nn.predict(&input);

        // Output should be single value between 0 and 1 (sigmoid)
        assert_eq!(output.len(), 1);
        assert!(output[0] > 0.0 && output[0] < 1.0);
    }

    #[test]
    fn test_xor_learning() {
        // XOR is classic non-linearly separable problem
        let inputs = vec![
            vec![0.0, 0.0],
            vec![0.0, 1.0],
            vec![1.0, 0.0],
            vec![1.0, 1.0],
        ];
        let targets = vec![
            vec![0.0],
            vec![1.0],
            vec![1.0],
            vec![0.0],
        ];

        let mut nn = NeuralNetwork::new(2, 4, 1, 0.5);

        // Train for many epochs
        nn.train(&inputs, &targets, 5000);

        // Check predictions
        for (input, target) in inputs.iter().zip(targets.iter()) {
            let output = nn.predict(input);
            // Should be within 0.3 of target
            assert!((output[0] - target[0]).abs() < 0.3);
        }
    }

    #[test]
    fn test_simple_pattern() {
        // Simple pattern: output = AND gate
        let inputs = vec![
            vec![0.0, 0.0],
            vec![0.0, 1.0],
            vec![1.0, 0.0],
            vec![1.0, 1.0],
        ];
        let targets = vec![
            vec![0.0],
            vec![0.0],
            vec![0.0],
            vec![1.0],
        ];

        let mut nn = NeuralNetwork::new(2, 3, 1, 0.5);
        nn.train(&inputs, &targets, 1000);

        // Should learn AND gate
        let output = nn.predict(&vec![1.0, 1.0]);
        assert!(output[0] > 0.7); // Should be close to 1

        let output = nn.predict(&vec![0.0, 0.0]);
        assert!(output[0] < 0.3); // Should be close to 0
    }

    #[test]
    fn test_mse_decreases() {
        let inputs = vec![
            vec![0.0, 0.0],
            vec![0.0, 1.0],
            vec![1.0, 0.0],
            vec![1.0, 1.0],
        ];
        let targets = vec![
            vec![0.0],
            vec![0.0],
            vec![0.0],
            vec![1.0],
        ];

        let mut nn = NeuralNetwork::new(2, 3, 1, 0.5);

        let mse_before = nn.mean_squared_error(&inputs, &targets);
        nn.train(&inputs, &targets, 500);
        let mse_after = nn.mean_squared_error(&inputs, &targets);

        // MSE should decrease with training
        assert!(mse_after < mse_before);
    }

    #[test]
    fn test_multiclass_classification() {
        // Simple multiclass: classify into 3 classes based on sum
        let inputs = vec![
            vec![0.0, 0.0], // sum=0 -> class 0
            vec![0.5, 0.0], // sum=0.5 -> class 1
            vec![1.0, 0.0], // sum=1 -> class 2
            vec![0.0, 0.5], // sum=0.5 -> class 1
            vec![0.5, 0.5], // sum=1 -> class 2
        ];
        let targets = vec![
            vec![1.0, 0.0, 0.0], // One-hot for class 0
            vec![0.0, 1.0, 0.0], // One-hot for class 1
            vec![0.0, 0.0, 1.0], // One-hot for class 2
            vec![0.0, 1.0, 0.0],
            vec![0.0, 0.0, 1.0],
        ];

        let mut nn = NeuralNetwork::new(2, 5, 3, 0.3);
        nn.train(&inputs, &targets, 2000);

        // Check that it learns something
        let mse = nn.mean_squared_error(&inputs, &targets);
        assert!(mse < 0.3);
    }

    #[test]
    fn test_single_output_regression() {
        // Learn f(x) ≈ x (identity function on [0,1])
        let inputs = vec![
            vec![0.0],
            vec![0.25],
            vec![0.5],
            vec![0.75],
            vec![1.0],
        ];
        let targets = vec![
            vec![0.0],
            vec![0.25],
            vec![0.5],
            vec![0.75],
            vec![1.0],
        ];

        let mut nn = NeuralNetwork::new(1, 3, 1, 0.5);
        nn.train(&inputs, &targets, 2000);

        // Test predictions
        let pred = nn.predict(&vec![0.5]);
        assert!((pred[0] - 0.5).abs() < 0.2);
    }

    #[test]
    fn test_batch_prediction() {
        let mut nn = NeuralNetwork::new(2, 3, 1, 0.1);

        let inputs = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
        ];

        // Should be able to predict for each input
        for input in inputs {
            let output = nn.predict(&input);
            assert_eq!(output.len(), 1);
        }
    }

    #[test]
    fn test_different_learning_rates() {
        let inputs = vec![
            vec![0.0],
            vec![1.0],
        ];
        let targets = vec![
            vec![0.0],
            vec![1.0],
        ];

        let mut nn_slow = NeuralNetwork::new(1, 2, 1, 0.01);
        nn_slow.train(&inputs, &targets, 100);
        let mse_slow = nn_slow.mean_squared_error(&inputs, &targets);

        let mut nn_fast = NeuralNetwork::new(1, 2, 1, 0.5);
        nn_fast.train(&inputs, &targets, 100);
        let mse_fast = nn_fast.mean_squared_error(&inputs, &targets);

        // Faster learning rate should achieve lower error in same epochs
        assert!(mse_fast < mse_slow);
    }

    #[test]
    fn test_accuracy_calculation() {
        let inputs = vec![
            vec![0.0, 0.0],
            vec![1.0, 1.0],
        ];
        let targets = vec![
            vec![1.0, 0.0], // Class 0
            vec![0.0, 1.0], // Class 1
        ];

        let mut nn = NeuralNetwork::new(2, 3, 2, 0.5);
        nn.train(&inputs, &targets, 1000);

        let accuracy = nn.accuracy(&inputs, &targets);

        // Should achieve reasonable accuracy
        assert!(accuracy >= 0.5);
    }

    #[test]
    fn test_overfitting_prevention() {
        // Small dataset - network should still work
        let inputs = vec![vec![0.5, 0.5]];
        let targets = vec![vec![1.0]];

        let mut nn = NeuralNetwork::new(2, 10, 1, 0.1);
        nn.train(&inputs, &targets, 100);

        let pred = nn.predict(&inputs[0]);
        // Should fit the single data point
        assert!((pred[0] - 1.0).abs() < 0.3);
    }
}
