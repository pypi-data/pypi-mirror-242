import numpy as np

from sz.core.tensor import Parameter
from sz.core.layer import Layer
from sz.accelerate.cuda import CUDA
from sz.functions.ft0 import linear


class Linear(Layer):

    # def __init__(self, out_size, nobias=False, dtype=np.float32, in_size=None):
    def __init__(self, out_size, nobias=False, dtype=np.float32):
        """
        假设x的形态为(100,35)，经过xW+b的变换会有一个输出如(100,15),那么W和b要取什么才能满足呢？
        首先W第一个必须要取35（即x.shape[1]），然后第二个就是要取输出的15（即(100,15).shape[1]），这样(100,35)*(35,15)就是(100,15)
        """
        super().__init__()
        # self.in_size = in_size
        self.in_size = None
        self.out_size = out_size
        self.dtype = dtype

        # 线性方程xW+b，因此需要参数W和b
        # 处理参数W
        self.W = Parameter(None, name='W')
        # if self.in_size is not None:
        #    self._init_W()
        # 处理参数b
        self.__init_b(nobias, dtype)

    def _init_W(self, xp=np):
        I, O = self.in_size, self.out_size
        W_data = xp.random.randn(I, O).astype(self.dtype) * np.sqrt(1 / I)
        self.W.data = W_data

    def __init_b(self, nobias, dtype):
        # 处理参数b
        if nobias:
            self.b = None
        else:
            """
            假设xW的形态为(100,25)，b要能与形态(100,25)相加，则b的形态最低限度取最后一位25
            参考：
            import numpy as np
            x = np.zeros((100, 25))
            y = np.zeros(25)
            print((x + y).shape)  # (100, 25)
            x = np.zeros((100, 25, 10))
            y = np.zeros(10)
            print((x + y).shape)  # (100, 25, 10)
            """
            self.b = Parameter(np.zeros(self.out_size, dtype=dtype), name='b')

    def forward(self, x):
        if self.W.data is None:
            self.in_size = x.shape[1]
            self._init_W(CUDA.to_gpu())
        y = linear(x, self.W, self.b)
        return y
