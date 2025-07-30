import torch
import torch.nn as nn
import torch.nn.functional as F

#入力チャネル
#黒石の位置      1
#白石の位置      1
#空白の位置      1
#40手前までの手 40
#合計           43

ch = 256

#biasクラスはdlshogiからの移植
class bias(nn.Module):
    def __init__(self, shape):
        super(bias, self).__init__()
        self.bias=nn.Parameter(torch.Tensor(shape))

    def forward(self, input):
        return input + self.bias

class block(nn.Module):
    def __init__(self):
        super(block, self).__init__()
        self.conv1 = nn.LazyConv2d(out_channels = ch, kernel_size = 3, padding = 1, bias = False)
        self.norm1 = nn.LazyBatchNorm2d(eps = 2e-05)
        self.conv2 = nn.LazyConv2d(out_channels = ch, kernel_size = 3, padding = 1, bias = False)
        self.norm2 = nn.LazyBatchNorm2d(eps = 2e-05)

    def forward(self, x):
        h1 = F.relu(self.norm1(self.conv1(x)))
        h2 = self.norm2(self.conv2(h1))
        return F.relu(x + h2)

class policy(nn.Module):
    def __init__(self):
        super(policy, self).__init__()
        self.batch_size = 1
        self.l1 = nn.LazyConv2d(out_channels = ch, kernel_size = 5, padding = 2, bias = False)
        self.n1 = nn.LazyBatchNorm2d(eps = 2e-05)
        self.b1 = block()
        self.b2 = block()
        self.b3 = block()
        self.b4 = block()
        self.b5 = block()
        self.b6 = block()
        self.b7 = block()
        self.b8 = block()
        self.l2 = nn.LazyConv2d(2, 1, 1, 0, 1, 1, False)
        self.l2_bias = bias(19)

    def forward(self, x):
        h = F.relu(self.n1(self.l1(x)))
        h = self.b1.forward(h)
        h = self.b2.forward(h)
        h = self.b3.forward(h)
        h = self.b4.forward(h)
        h = self.b5.forward(h)
        h = self.b6.forward(h)
        h = self.b7.forward(h)
        h = self.b8.forward(h)
        h = self.l2(h)
        h = self.l2_bias(h)
        h = h.reshape(self.batch_size, 2, 361)
        return h