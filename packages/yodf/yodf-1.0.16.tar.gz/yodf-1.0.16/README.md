## A 'Hello, World!' forward mode autodiff library.

This small (~500 lines) library is meant as an illustration of how forward mode autodiff can possibly be implemented. It lets you compute the value and the derivative of a function expressed as a computational flow using the primitives provided by the library. Interface of the library is very similar to Tensorflow 1.\*. With Tensorflow 1.\*, all the samples provided in _examples_ folder can very well be run if you do **import tensorflow as tf** as opposed to **import yodf as tf** It supports following operations { "add", "subtract", "divide", "multiply", "pow", "sin", "cos", "log", "exp", "matmul", "sigmoid", "reduce_mean", "reduce_sum" }.

### Installation

**pip install yodf** will install the library. Only dependency it has is _numpy_. Samples provided in examples folder also have dependency on _matplotlib_ and _scipy_.

### Basic usage

Below code computes the value and the derivative of the function **x^2** at x=5.0

```
import yodf as tf
x = tf.Variable(5.0)
cost = x**2
with tf.Session() as s:
    # global_variables_initializer API added just so as to
    # resemble Tensorflow, it hardly does anything
    s.run(tf.global_variables_initializer())
    s.run(cost)
print(x.value, cost.value, cost.gradient)

## Output
## 5.0 25.0 10.0
```

### Basic gradient descent example

Below code computes optima of the function **x^2** along with the value at which optima occurs starting with x=5.0

```
import yodf as tf
x = tf.Variable(5.0)
cost = x**2
train = tf.train.GradientDescentOptimizer(learning_rate=0.2).minimize(cost)
with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    for _ in range(50):
        _, cost_final, x_final = s.run([train, x, cost])
print(f"Minima: {cost_final:.10f}, x at minima: {x_final:.10f}")

## Output
## Minima: 0.0000000000, x at minima: 0.0000000000
```

## How does it work?

It has a class called _Tensor_ with _Variable_ and _\_Constant_ as subclasses. Tensor object holds a value and a gradient. Gradient of a constant is 0 and that of a variable is 1 which is as good as saying d(x)/dx.  
A tensor can also represent an operation and a tensor representating an operation gets created using a convenient function call like _tf.sin()_ or _tf.matmul()_ etc.

```
import numpy as np
import yodf as tf
x = tf.Variable(np.array([[1,1],[2,2]]))
op_sin = tf.sin(x)
print(op_sin)

## Output
## <yod.Tensor type=TensorType.INT, shape=(2, 2), operation='sin'>
```

You typically pass a tensor to run method of _Session_ class which ends up evaluating the tensor along with its derivative. Execute method of tensor just knows how to compute derivative of basic arithmatic operations, power function and some of the transcendental functions like sin, cos, log, exp. It also knows how to compute derivative when matrix multiplication operation is involved. By applying the chain rule repeatedly to these operations, derivative of an arbitrary function (represented as a tensor) gets computed automatically. _run_ method simply builds post order traversal tree of the tensor passed to it and evaluates all the nodes in the tree. _GradientDescentOptimizer_ simply updates the value of the variable based on the gradient of the cost tensor passed to its minimize function.  
With multiple independent variables, partial derivative of one variable gets computed at a time while the gradient of rest of the variables is set to 0. This, in turn, is done for all the variables and partial derivatives or the gradients of all the vatiables are accumulated by _GradientDescentOptimizer_ which is not necessarily very clean.

## Examples

Examples folder shows use of this library for

1. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example1_simple_cost_function.ipynb">A gradient descent problem for a simple cost function</a>
2. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example2_cost_function_2_variables.ipynb">A gradient descent problem for a simple cost function with 2 independent variables</a>
3. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example3_linear_regression.ipynb">A linear regression problem</a>
4. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example4_linear_regression_sin_x.ipynb">A linear regression problem, fitting sin(x)</a>
5. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example5_logistic_regression.ipynb">A logistic regression problem</a>
6. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example6_neural_network.ipynb">A neural network with one hidden layer and one output</a>
7. <a href="https://github.com/yogimogi/yodf/blob/master/examples/example7_neural_network_mnist.ipynb">A neural network with one hidden layer and 10 outputs (MNIST digit classification)</a>

## Limitiation of forward mode autodiff

Though with forward mode autodiff, derivative of a function with one independent variables gets computed during forward pass itself and no backward pass is needed as is the case with reverse mode autodiff (generalized backpropagation), with multiple indepdent variables (say weights in a neural network), as many passes are needed as number of indepdent variables. So as can be seen in <a href="https://github.com/yogimogi/yodf/blob/master/examples/example3_linear_regression.ipynb">linear regression sample</a>, time needed by gradient descent linearly increases with increase in degree of polynomial you are trying to fit. For MNIST digit classification, this library becomes almost unusable due to large number of independent variables whose gradient needs to be computed. Machine learning frameworks like PyTorch, TensorFlow, Theano use reverse mode autodiff for gradient computation
