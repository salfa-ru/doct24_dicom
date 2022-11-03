from miscnn.data_loading.interfaces import NIFTI_interface
from miscnn import Data_IO, Preprocessor, Neural_Network
from miscnn.processing.subfunctions import Normalization, Clipping, Resampling
from miscnn.neural_network.architecture.unet.standard import Architecture


def covid_model(input_path, output_path):
    interface = NIFTI_interface(channels=1, classes=4)
    data_io = Data_IO(interface, input_path=input_path, output_path=output_path,
                      delete_batchDir=False)
    sf_clipping = Clipping(min=-1250, max=250)
    sf_normalize = Normalization(mode="grayscale")
    sf_resample = Resampling((1.58, 1.58, 2.70))
    sf_zscore = Normalization(mode="z-score")
    sf = [sf_clipping, sf_normalize, sf_resample, sf_zscore]
    pp = Preprocessor(data_io, data_aug=None, batch_size=2, subfunctions=sf,
                      prepare_subfunctions=True, prepare_batches=False,
                      analysis="patchwise-crop", patch_shape=(160, 160, 80),
                      use_multiprocessing=True)
    pp.patchwise_overlap = (80, 80, 30)
    pp.mp_threads = 16
    unet_standard = Architecture(depth=4, activation="softmax",
                                 batch_normalization=True)
    model = Neural_Network(preprocessor=pp, architecture=unet_standard)
    path_model = './models/covid_model.hdf5'
    model.load(path_model)
    return model
