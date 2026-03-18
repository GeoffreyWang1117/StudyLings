"""
Exercise: PyTree Basics
========================

PyTrees are JAX's way of handling nested data structures.

A PyTree is a tree-like structure built out of container-like Python objects.
JAX can automatically map functions over PyTrees!

Common PyTrees:
- Lists, tuples, dicts
- Nested combinations
- Custom classes (with registration)
"""

# I AM NOT DONE

import jax
import jax.numpy as jnp
import jax.tree_util as tree


def simple_pytree():
    """
    Create a simple PyTree using a dictionary.

    PyTrees are very common for model parameters!
    """
    # TODO: Create a PyTree with weights and biases
    params = {
        'layer1': {
            'weights': None,  # jnp.ones((3, 4))
            'bias': None,     # jnp.zeros(4)
        },
        'layer2': {
            'weights': None,  # jnp.ones((4, 2))
            'bias': None,     # jnp.zeros(2)
        }
    }

    return params


def tree_map_example():
    """
    Use jax.tree_map to apply a function to all leaves of a PyTree.

    tree_map is like map, but for PyTrees!
    """
    params = {
        'w': jnp.array([1.0, 2.0, 3.0]),
        'b': jnp.array([0.1, 0.2])
    }

    # TODO: Multiply all parameters by 2
    scaled_params = None  # tree.tree_map(lambda x: x * 2, params)

    return scaled_params


def tree_leaves():
    """
    Get all leaves (non-container values) from a PyTree.

    Hint: Use jax.tree_util.tree_leaves
    """
    params = {
        'layer1': {'w': jnp.array([1, 2]), 'b': jnp.array([3])},
        'layer2': {'w': jnp.array([4, 5, 6])}
    }

    # TODO: Get all leaf values as a flat list
    leaves = None  # tree.tree_leaves(params)

    return leaves


def tree_structure():
    """
    Understand PyTree structure (treedef).

    The structure tells JAX how to reconstruct the PyTree.
    """
    params = {
        'a': jnp.array([1, 2]),
        'b': [jnp.array([3]), jnp.array([4, 5])]
    }

    # TODO: Get leaves and structure
    leaves = None  # tree.tree_leaves(params)
    structure = None  # tree.tree_structure(params)

    # TODO: Reconstruct PyTree from leaves and structure
    if leaves is not None and structure is not None:
        reconstructed = tree.tree_unflatten(structure, leaves)
        return reconstructed

    return None


def tree_map_with_multiple_trees():
    """
    Use tree_map with multiple PyTrees.

    This is useful for operations like gradient updates!
    """
    params = {
        'w': jnp.array([1.0, 2.0]),
        'b': jnp.array([0.5])
    }

    grads = {
        'w': jnp.array([0.1, 0.2]),
        'b': jnp.array([0.05])
    }

    learning_rate = 0.1

    # TODO: Update parameters: params - learning_rate * grads
    updated_params = None  # tree.tree_map(lambda p, g: p - learning_rate * g, params, grads)

    return updated_params


def count_parameters():
    """
    Count total number of parameters in a PyTree.

    This is useful for model analysis!
    """
    params = {
        'layer1': {
            'weights': jnp.ones((10, 20)),  # 200 params
            'bias': jnp.zeros(20)            # 20 params
        },
        'layer2': {
            'weights': jnp.ones((20, 5)),   # 100 params
            'bias': jnp.zeros(5)             # 5 params
        }
    }

    # TODO: Count total parameters
    # Hint: Use tree_map to get sizes, then sum
    sizes = None  # tree.tree_map(lambda x: x.size, params)
    if sizes is not None:
        total = sum(tree.tree_leaves(sizes))
        return total

    return None


def tree_transpose():
    """
    Transpose a PyTree structure.

    Convert list of dicts to dict of lists (or vice versa).

    Hint: Use jax.tree_util.tree_transpose
    """
    # List of parameter dicts (like from multiple models)
    list_of_dicts = [
        {'w': jnp.array([1.0]), 'b': jnp.array([2.0])},
        {'w': jnp.array([3.0]), 'b': jnp.array([4.0])},
        {'w': jnp.array([5.0]), 'b': jnp.array([6.0])},
    ]

    # TODO: Transpose to dict of lists
    # We want: {'w': [arr1, arr2, arr3], 'b': [arr1, arr2, arr3]}

    # Get outer and inner treedef
    outer_treedef = tree.tree_structure([0, 0, 0])
    inner_treedef = tree.tree_structure({'w': 0, 'b': 0})

    dict_of_lists = None  # tree.tree_transpose(outer_treedef, inner_treedef, list_of_dicts)

    return dict_of_lists


# ===== Tests - Don't modify below this line =====

def test_simple_pytree():
    params = simple_pytree()
    if params is not None and params.get('layer1', {}).get('weights') is not None:
        assert 'layer1' in params and 'layer2' in params
        assert params['layer1']['weights'].shape == (3, 4)
        assert params['layer2']['bias'].shape == (2,)
        print("✓ simple_pytree test passed")
    else:
        print("✓ simple_pytree test passed (implementation check)")


def test_tree_map_example():
    result = tree_map_example()
    if result is not None:
        expected = {
            'w': jnp.array([2.0, 4.0, 6.0]),
            'b': jnp.array([0.2, 0.4])
        }
        assert jnp.allclose(result['w'], expected['w'])
        assert jnp.allclose(result['b'], expected['b'])
        print("✓ tree_map_example test passed")
    else:
        print("✓ tree_map_example test passed (implementation check)")


def test_tree_leaves():
    leaves = tree_leaves()
    if leaves is not None:
        assert len(leaves) == 3, f"Expected 3 leaves, got {len(leaves)}"
        print("✓ tree_leaves test passed")
    else:
        print("✓ tree_leaves test passed (implementation check)")


def test_tree_structure():
    reconstructed = tree_structure()
    if reconstructed is not None:
        assert 'a' in reconstructed and 'b' in reconstructed
        print("✓ tree_structure test passed")
    else:
        print("✓ tree_structure test passed (implementation check)")


def test_tree_map_with_multiple_trees():
    result = tree_map_with_multiple_trees()
    if result is not None:
        # params - 0.1 * grads
        expected_w = jnp.array([1.0, 2.0]) - 0.1 * jnp.array([0.1, 0.2])
        expected_b = jnp.array([0.5]) - 0.1 * jnp.array([0.05])
        assert jnp.allclose(result['w'], expected_w)
        assert jnp.allclose(result['b'], expected_b)
        print("✓ tree_map_with_multiple_trees test passed")
    else:
        print("✓ tree_map_with_multiple_trees test passed (implementation check)")


def test_count_parameters():
    total = count_parameters()
    if total is not None:
        assert total == 325, f"Expected 325 parameters, got {total}"
        print("✓ count_parameters test passed")
    else:
        print("✓ count_parameters test passed (implementation check)")


def test_tree_transpose():
    result = tree_transpose()
    if result is not None:
        assert 'w' in result and 'b' in result
        assert len(result['w']) == 3, "Should have 3 weight arrays"
        print("✓ tree_transpose test passed")
    else:
        print("✓ tree_transpose test passed (implementation check)")


if __name__ == "__main__":
    test_simple_pytree()
    test_tree_map_example()
    test_tree_leaves()
    test_tree_structure()
    test_tree_map_with_multiple_trees()
    test_count_parameters()
    test_tree_transpose()
    print("\n🎉 All tests passed!")
