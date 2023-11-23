import numpy as np

x = np.zeros((100, 25))
y = np.zeros(25)
print((x + y).shape)  # (100, 25)
x = np.zeros((100, 25, 10))
y = np.zeros(10)
print((x + y).shape)  # (100, 25, 10)


I, O = 10, 25
W_data = np.random.randn(I, O).astype(np.float32) * np.sqrt(1 / I)
print(W_data.shape)
