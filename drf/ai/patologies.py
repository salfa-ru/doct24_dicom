import pickle
import numpy as np


class Piece():
    def __init__(self, masked_array=np.ma.MaskedArray(), point=None):
        self.data = masked_array.data
        self.mask = masked_array.mask
        self.point = point
        self.shape = self.data.shape

    def __getitem__(self, item):
        return np.ma.MaskedArray(self.data[item], self.mask[item])

    def dump(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


if __name__ == "__main__":
    p = Piece()
