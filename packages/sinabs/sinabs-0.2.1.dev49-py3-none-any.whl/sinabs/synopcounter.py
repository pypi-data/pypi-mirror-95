import torch
from sinabs.layers import NeuromorphicReLU
from numpy import product
import pandas as pd


def synops_hook(layer, inp, out):
    assert len(inp) == 1, "Multiple inputs not supported for synops hook"
    inp = inp[0]
    layer.tot_in = inp.sum().item()
    layer.tot_out = out.sum().item()
    layer.synops = layer.tot_in * layer.fanout
    layer.tw = inp.shape[0]


class SNNSynOpCounter:
    """
    Counter for the synaptic operations emitted by all SpikingLayers in a
    spiking model.
    Note that this is automatically instantiated by `from_torch` and by
    `Network` if they are passed `synops=True`.

    Usage:
        counter = SNNSynOpCounter(my_spiking_model)

        output = my_spiking_model(input)  # forward pass

        synops_table = counter.get_synops()

    Arguments:
        model: Spiking model.
        dt: the number of milliseconds corresponding to a time step in the \
        simulation (default 1.0).
    """
    def __init__(self, model, dt=1.0):
        self.model = model
        self.handles = []
        self.dt = dt

        for layer in model.modules():
            self._register_synops_hook(layer)

    def _register_synops_hook(self, layer):
        if isinstance(layer, torch.nn.Conv2d):
            layer.fanout = (layer.out_channels *
                            product(layer.kernel_size) /
                            product(layer.stride))
        elif isinstance(layer, torch.nn.Linear):
            layer.fanout = layer.out_features
        else:
            return None

        handle = layer.register_forward_hook(synops_hook)
        self.handles.append(handle)

    def get_synops(self) -> pd.DataFrame:
        """
        Method to compute a table of synaptic operations for the latest forward pass.

        NOTE: this may not be accurate in presence of average pooling.

        Returns:
            SynOps_dataframe: A Pandas DataFrame containing layer IDs and \
            respectively, for the latest forward pass performed, their:
                number of input spikes,
                fanout,
                synaptic operations,
                number of timesteps,
                total duration of simulation,
                number of synaptic operations per second.
        """
        SynOps_dataframe = pd.DataFrame()
        for i, lyr in enumerate(self.model.modules()):
            if hasattr(lyr, 'synops'):
                SynOps_dataframe = SynOps_dataframe.append(
                    pd.Series(
                        {
                            "Layer": i,
                            "In": lyr.tot_in,
                            "Fanout_Prev": lyr.fanout,
                            "SynOps": lyr.synops,
                            "N. timesteps": lyr.tw,
                            "Time window (ms)": lyr.tw * self.dt,
                            "SynOps/s": lyr.synops / lyr.tw / self.dt * 1000,
                        }
                    ),
                    ignore_index=True,
                )
        SynOps_dataframe.set_index("Layer", inplace=True)
        return SynOps_dataframe

    def get_total_power_use(self, j_per_synop=1e-11):
        """
        Method to quickly get the total power use of the network, estimated
        over the latest forward pass.

        Arguments:
            j_per_synop: Energy use per synaptic operation, in joules.\
            Default 1e-11 J.

        Returns: estimated power in mW.
        """
        synops_table = self.get_synops()
        tot_synops_per_s = synops_table["SynOps/s"].sum()
        power_in_mW = tot_synops_per_s * j_per_synop * 1000
        return power_in_mW

    def __del__(self):
        for handle in self.handles:
            handle.remove()


class SynOpCounter(object):
    """
    Counter for the synaptic operations emitted by all Neuromorphic ReLUs in an
    analog CNN model.

    Usage:
        counter = SynOpCounter(MyTorchModel.modules(), sum_activations=True)

        output = MyTorchModule(input)  # forward pass

        synop_count = counter()

    :param modules: list of modules, e.g. MyTorchModel.modules()
    :param sum_activations: If True (default), returns a single number of synops, otherwise a list of layer synops.
    """

    def __init__(self, modules, sum_activations=True):
        self.modules = []
        for module in modules:
            if isinstance(module, NeuromorphicReLU) and module.fanout > 0:
                self.modules.append(module)

        if len(self.modules) == 0:
            raise ValueError("No NeuromorphicReLU found in module list.")

        self.sum_activations = sum_activations
        # self.modules[1:] = []

    def __call__(self):
        synops = []
        for module in self.modules:
            synops.append(module.activity)

        if self.sum_activations:
            synops = torch.stack(synops).sum()
        return synops
