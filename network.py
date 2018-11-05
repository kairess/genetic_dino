import numpy as np

class Network:
  def __init__(self):
    self.input_size = 2
    self.hidden_size = 8
    self.hidden2_size = 4
    self.output_size = 1
    self.W1 = np.random.randn(self.input_size, self.hidden_size)
    self.W2 = np.random.randn(self.hidden_size, self.hidden2_size)
    self.W3 = np.random.randn(self.hidden2_size, self.output_size)
    # self.W1 = np.ones((self.input_size, self.hidden_size))
    # self.W2 = np.ones((self.hidden_size, self.hidden2_size))
    # self.W3 = np.ones((self.hidden2_size, self.output_size))
    self.fitness = 0

  def forward(self, inputs):
    z1 = np.dot(inputs, self.W1)
    a1 = np.tanh(z1)
    z2 = np.dot(a1, self.W2)
    a2 = np.tanh(z2)
    z3 = np.dot(a2, self.W3)
    yHat = np.tanh(z3)
    return yHat

  def sigmoid(self, z):
    return 1 / (1 + np.exp(-z))

  def relu(self, z):
    return z * (z > 0)
