import torch.nn as nn
from .functional import quantize


class QuantizeLayer(nn.Module):
    """
    Layer that quantizes the input, i.e. returns floor(input).

    :param quantize: If False, this layer will do nothing.
    """

    def __init__(self, quantize=True):
        super().__init__()
        self.quantize = quantize

    def forward(self, data):
        if self.quantize:
            return quantize(data)
        else:
            return data
