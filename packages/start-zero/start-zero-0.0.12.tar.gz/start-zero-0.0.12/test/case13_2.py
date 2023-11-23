import numpy as np
import matplotlib.pyplot as plt

from sz import LinearLayer, clear_layers_tensors
from sz import sigmoid, mean_squared_error

np.random.seed(0)
x = np.random.rand(100, 1)  # 100行1列
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)  # 100行1列

l1 = LinearLayer(10)
l2 = LinearLayer(1)


def predict(X):
    Y = l1(X)
    Y = sigmoid(Y)
    Y = l2(Y)
    return Y


lr = 0.2
epoch = 10000

for i in range(epoch):

    y_grad = predict(x)
    loss = mean_squared_error(y, y_grad)
    # l1.clear_tensors()
    # l2.clear_tensors()
    clear_layers_tensors(l1, l2)
    loss.backward()

    for l in [l1, l2]:
        for p in l.params():
            p.data -= lr * p.grad.data
    if i % 1000 == 0:
        print(loss)

# Plot
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
t = np.arange(0, 1, .01)[:, np.newaxis]
y_pred = predict(t)
plt.plot(t, y_pred.data, color='r')
plt.show()
"""
Tensor(0.8473695850105871)
Tensor(0.2514286285183607)
Tensor(0.24759485466749878)
Tensor(0.23786120447054832)
Tensor(0.21222231333102953)
Tensor(0.16742181117834223)
Tensor(0.0968193261999272)
Tensor(0.07849528290602335)
Tensor(0.07749729552991157)
Tensor(0.07722132399559317)
"""
