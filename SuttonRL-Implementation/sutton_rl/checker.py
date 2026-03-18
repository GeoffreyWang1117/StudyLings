"""
Exercise checker - validates exercise results
"""
from typing import Dict, Any, Optional
import numpy as np


class ExerciseChecker:
    """Checks exercise results against expected criteria"""

    def __init__(self):
        # Define acceptance criteria for each exercise
        self.criteria = {
            # Chapter 2: Bandits
            'ch02_ex01_epsilon_greedy': {
                'avg_reward_min': 1.2,
                'avg_reward_max': 1.6,
                'optimal_action_pct_min': 0.7,
            },
            'ch02_ex02_ucb': {
                'avg_reward_min': 1.3,
                'avg_reward_max': 1.7,
                'optimal_action_pct_min': 0.75,
            },
            'ch02_ex03_gradient_bandit': {
                'avg_reward_min': 1.2,
                'avg_reward_max': 1.6,
                'optimal_action_pct_min': 0.65,
            },
            'ch02_ex04_optimistic_initial': {
                'avg_reward_min': 1.2,
                'avg_reward_max': 1.6,
                'exploration_early': True,
            },

            # Chapter 4: Dynamic Programming
            'ch04_ex01_policy_evaluation': {
                'value_error_max': 0.1,
                'converges': True,
            },
            'ch04_ex02_policy_iteration': {
                'value_error_max': 0.1,
                'policy_optimal': True,
                'iterations_max': 100,
            },
            'ch04_ex03_value_iteration': {
                'value_error_max': 0.1,
                'policy_optimal': True,
                'iterations_max': 100,
            },
            'ch04_ex04_gamblers_problem': {
                'value_error_max': 0.1,
                'policy_reasonable': True,
            },

            # Chapter 5: Monte Carlo
            'ch05_ex01_first_visit_mc': {
                'value_error_max': 0.2,
                'converges': True,
            },
            'ch05_ex02_mc_es': {
                'policy_improves': True,
                'return_threshold': 0.0,
            },
            'ch05_ex03_off_policy_mc': {
                'value_error_max': 0.3,
                'converges': True,
            },

            # Chapter 6: Temporal-Difference
            'ch06_ex01_td0': {
                'value_error_max': 0.2,
                'converges': True,
            },
            'ch06_ex02_sarsa': {
                'avg_return_min': -100,
                'converges': True,
            },
            'ch06_ex03_q_learning': {
                'avg_return_min': -100,
                'converges': True,
                'finds_optimal': True,
            },
            'ch06_ex04_expected_sarsa': {
                'avg_return_min': -100,
                'converges': True,
            },

            # Chapter 7: n-step
            'ch07_ex01_n_step_td': {
                'value_error_max': 0.2,
                'converges': True,
            },
            'ch07_ex02_n_step_sarsa': {
                'avg_return_min': -100,
                'converges': True,
            },

            # More chapters will be added...
        }

    def check_result(self, exercise_id: str, result: Dict[str, Any]) -> bool:
        """
        Check if exercise result meets criteria

        Args:
            exercise_id: Exercise identifier
            result: Dictionary containing test results

        Returns:
            True if all criteria are met, False otherwise
        """
        if exercise_id not in self.criteria:
            # If no criteria defined, just check if result exists and is not None
            return result is not None

        criteria = self.criteria[exercise_id]
        checks_passed = 0
        checks_total = 0

        for key, expected in criteria.items():
            checks_total += 1

            if key.endswith('_min'):
                actual_key = key[:-4]  # Remove '_min' suffix
                if actual_key in result:
                    if result[actual_key] >= expected:
                        checks_passed += 1
                        print(f"  ✓ {actual_key}: {result[actual_key]:.4f} >= {expected:.4f}")
                    else:
                        print(f"  ✗ {actual_key}: {result[actual_key]:.4f} < {expected:.4f}")

            elif key.endswith('_max'):
                actual_key = key[:-4]  # Remove '_max' suffix
                if actual_key in result:
                    if result[actual_key] <= expected:
                        checks_passed += 1
                        print(f"  ✓ {actual_key}: {result[actual_key]:.4f} <= {expected:.4f}")
                    else:
                        print(f"  ✗ {actual_key}: {result[actual_key]:.4f} > {expected:.4f}")

            elif isinstance(expected, bool):
                if key in result:
                    if result[key] == expected:
                        checks_passed += 1
                        print(f"  ✓ {key}: {result[key]}")
                    else:
                        print(f"  ✗ {key}: {result[key]} (expected {expected})")

            else:
                if key in result:
                    if np.allclose(result[key], expected, rtol=0.1):
                        checks_passed += 1
                        print(f"  ✓ {key}: matches expected")
                    else:
                        print(f"  ✗ {key}: does not match expected")

        print(f"\n检查通过: {checks_passed}/{checks_total}")

        return checks_passed == checks_total

    def add_criteria(self, exercise_id: str, criteria: Dict[str, Any]):
        """Add criteria for a new exercise"""
        self.criteria[exercise_id] = criteria
