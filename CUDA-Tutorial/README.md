# JAXlings 🔥

**Interactive JAX learning exercises with automatic grading** - inspired by Rustlings!

JAXlings is a comprehensive tutorial system designed to teach JAX from beginner to advanced levels through hands-on coding exercises.

## 🎯 What is JAXlings?

JAXlings helps you learn JAX by fixing small exercises. Each exercise is designed to teach you a specific concept in JAX, from basic array operations to advanced topics like ResNet, Transformers, and parallel computation.

## ✨ Features

- **35+ exercises** covering JAX from basics to advanced topics
- **Automatic grading** - instant feedback on your solutions
- **Watch mode** - automatically re-runs exercises when you save
- **Progressive difficulty** - from intro to expert level
- **Real-world examples** - ResNet, complete Transformer, parallel training
- **Comprehensive coverage**:
  - Introduction to JAX arrays and operations
  - Array manipulation (indexing, reshaping, broadcasting)
  - Automatic differentiation with `grad`
  - JIT compilation for performance
  - Vectorization with `vmap`
  - JAX random number system (PRNG)
  - PyTree data structures
  - Control flow primitives (cond, scan, while_loop)
  - Parallel computation with `pmap`
  - Neural network building blocks
  - Optimizers (SGD, Adam, RMSprop)
  - Advanced architectures (ResNet, complete Transformer)

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jaxlings.git
cd jaxlings

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Quick Start

```bash
# Run the next pending exercise
python jaxlings.py verify

# Or use the installed command
jaxlings verify
```

## 📚 How to Use

### Basic Commands

```bash
# Verify the next exercise
jaxlings verify

# Watch mode - automatically run when files change
jaxlings watch

# Run a specific exercise
jaxlings run intro01_hello_jax

# List all exercises
jaxlings list

# Get a hint for the current exercise
jaxlings hint

# Get a hint for a specific exercise
jaxlings hint arrays01_indexing

# Reset all progress
jaxlings reset
```

### Workflow

1. **Start with the first exercise:**
   ```bash
   jaxlings verify
   ```

2. **Open the exercise file** in your editor (the path will be shown)

3. **Read the instructions** and fix the code

4. **Remove the `# I AM NOT DONE` comment** when you think you're done

5. **Run the exercise** again:
   ```bash
   jaxlings verify
   ```

6. **Use watch mode** for automatic feedback:
   ```bash
   jaxlings watch
   ```

## 📖 Exercise Structure

Exercises are organized into 10 categories with 35+ total exercises:

### 01. Introduction (3 exercises)
- `intro01_hello_jax` - Getting started with JAX
- `intro02_arrays` - Creating JAX arrays
- `intro03_operations` - Basic array operations

### 02. Arrays (4 exercises)
- `arrays01_indexing` - Array indexing and slicing
- `arrays02_reshaping` - Reshaping and transposing
- `arrays03_broadcasting` - Broadcasting rules
- `arrays04_advanced_indexing` - Functional updates with `.at[]`

### 03. Transformations (5 exercises)
- `transform01_grad` - Automatic differentiation
- `transform02_value_and_grad` - Computing values and gradients
- `transform03_jit` - JIT compilation for speed
- `transform04_vmap` - Automatic vectorization
- `transform05_combining` - Combining transformations

### 04. Neural Networks (5 exercises)
- `nn01_linear_layer` - Building linear layers
- `nn02_activation` - Activation functions
- `nn03_loss_functions` - Loss functions
- `nn04_simple_mlp` - Multi-layer perceptrons
- `nn05_training_loop` - Training loops and optimization

### 05. Advanced (5 exercises)
- `advanced01_custom_grad` - Custom gradients with `custom_vjp`
- `advanced02_optimizer` - Implementing optimizers
- `advanced03_cnn` - Convolutional neural networks
- `advanced04_batch_norm` - Batch normalization
- `advanced05_attention` - Attention mechanisms

### 06. Random Numbers (2 exercises)
- `random01_prng_basics` - PRNG keys and basic sampling
- `random02_advanced_sampling` - Advanced distributions and techniques

### 07. PyTrees (1 exercise)
- `pytree01_basics` - Working with nested data structures

### 08. Control Flow (2 exercises)
- `control01_cond` - Conditional operations with `lax.cond`
- `control02_scan` - Efficient loops with `lax.scan`

### 09. Parallel Computation (1 exercise)
- `parallel01_pmap` - Data parallelism across devices

### 10. Deep Learning Advanced (2 exercises)
- `dl01_resnet_block` - ResNet residual blocks
- `dl02_transformer_complete` - Complete Transformer implementation

## 🎓 Learning Path

**Beginner** (01-02: Intro + Arrays)
→ **Intermediate** (03-04: Transformations + Neural Networks)
→ **Advanced** (05-06: Advanced Topics + Random Numbers)
→ **Expert** (07-10: PyTrees + Control Flow + Parallel + Deep Learning)

Each exercise builds on previous concepts, so we recommend following the order!

## 💡 Tips

- **Read the hints!** Use `jaxlings hint` when stuck
- **Run tests locally** - each exercise file can be run with `python exercises/.../exercise.py`
- **Use watch mode** - `jaxlings watch` gives instant feedback
- **Read JAX docs** - https://jax.readthedocs.io/
- **Don't skip exercises** - each one teaches important concepts

## 🧪 Running Tests

Each exercise file can be run independently:

```bash
python exercises/01_intro/intro01_hello_jax.py
```

Or run all tests:

```bash
pytest exercises/
```

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

- Add new exercises
- Improve existing exercises
- Fix bugs
- Improve documentation
- Share your learning experience

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Inspired by [Rustlings](https://github.com/rust-lang/rustlings)
- Built with [JAX](https://github.com/google/jax)
- Thanks to the JAX team for creating an amazing library!

## 📚 Resources

- [JAX Documentation](https://jax.readthedocs.io/)
- [JAX GitHub](https://github.com/google/jax)
- [JAX Tutorials](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html)

## 🎯 What You'll Learn

By completing JAXlings, you'll master:

- ✅ JAX array operations and NumPy compatibility
- ✅ Automatic differentiation and gradient computation
- ✅ JIT compilation for performance optimization
- ✅ Vectorization with vmap for efficient batching
- ✅ JAX's unique random number system (PRNG keys)
- ✅ PyTree data structures for complex parameters
- ✅ Control flow primitives (cond, scan, while_loop)
- ✅ Parallel computation across multiple devices (pmap)
- ✅ Building neural networks from scratch
- ✅ Implementing modern optimizers (SGD, Adam, RMSprop)
- ✅ Creating CNNs, ResNet, and complete Transformer architectures
- ✅ Advanced topics: custom gradients, batch normalization, multi-head attention
- ✅ Best practices for production JAX code

## 🚀 Next Steps

After completing JAXlings, check out:

- [Flax](https://github.com/google/flax) - Neural network library for JAX
- [Optax](https://github.com/deepmind/optax) - Gradient processing and optimization library
- [Haiku](https://github.com/deepmind/dm-haiku) - Neural network library by DeepMind
- [Equinox](https://github.com/patrick-kidger/equinox) - Elegant neural networks in JAX

---

**Happy Learning! 🎉**

If you find JAXlings helpful, please give it a star ⭐!
