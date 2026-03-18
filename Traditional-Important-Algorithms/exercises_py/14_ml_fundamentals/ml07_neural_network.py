# I AM NOT DONE

"""
Simple Neural Network

Feedforward neural network with backpropagation.

Your task: Implement neural network.
"""

import math
from typing import List


class NeuralNetwork:
    def __init__(self, layer_sizes: List[int]):
        self.layer_sizes = layer_sizes
        self.weights: List[List[List[float]]] = []
        self.biases: List[List[float]] = []

    @staticmethod
    def sigmoid(x: float) -> float:
        # TODO: Implement sigmoid
        pass

    @staticmethod
    def sigmoid_derivative(x: float) -> float:
        # TODO: Implement derivative
        pass

    def forward(self, x: List[float]) -> List[float]:
        """Forward pass"""
        # TODO: Implement forward pass
        pass

    def train(self, x: List[List[float]], y: List[List[float]], 
             learning_rate: float, epochs: int):
        """Train network"""
        # TODO: Implement training
        pass


import unittest

class TestNeuralNetwork(unittest.TestCase):
    def test_sigmoid(self):
        self.assertAlmostEqual(NeuralNetwork.sigmoid(0), 0.5)

if __name__ == '__main__':
    unittest.main()
