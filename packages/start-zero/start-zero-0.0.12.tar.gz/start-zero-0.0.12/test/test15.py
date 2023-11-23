import numpy as np

from sz import Tensor, Parameter, is_parameter, Layer

x = Tensor(np.array([1, 2]))
y = Parameter(np.array([10, 20]))
z = x + y
print(z)
print(is_parameter(x))
print(is_parameter(y))
print(is_parameter(z))
print('----------')
print(isinstance(10, (list, int)))
print('----------')
layer = Layer()
layer.a = "abc"
layer.b = x
layer.c = y
layer.d = z
layer.e = 1024
print(layer.params())
