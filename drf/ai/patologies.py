import pickle
import numpy as np


class Piece():
    def __init__(self, masked_array=np.ma.MaskedArray(), point=None):
        self.data = masked_array.data
        self.mask = masked_array.mask
        self.point = point
        self.shape = self.data.shape
        self.coef = self.mask

    def __getitem__(self, item):
        masked_array = np.ma.MaskedArray(self.data[item], self.mask[item])
        piece = Piece(masked_array, self.point)
        piece.coef = self.coef[item]
        return piece

    def dump(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def scaling(self, ratio=5):
        new_data = np.zeros(shape=(ratio * self.shape[0] + 1, self.shape[1], self.shape[2]))
        new_mask = np.zeros(shape=(ratio * self.shape[0] + 1, self.shape[1], self.shape[2]))
        new_coef = np.zeros(shape=(ratio * self.shape[0] + 1, self.shape[1], self.shape[2]), dtype=np.float16)
        for n in np.arange(self.shape[0] - 1):
            new_data[n * ratio] = self.data[n]
            new_mask[n * ratio] = self.mask[n]
            new_coef[n * ratio] = self.coef[n]
            data_step = (self.data[n] - self.data[n + 1]) // ratio
            for i in np.arange(1, ratio):
                new_data[n * ratio + i] = self.data[n] + data_step * i
                new_mask[n * ratio + i] = self.mask[n] if i < 0.5 * ratio else self.mask[n + 1]
                new_coef[n * ratio + i] = self.coef[n] if i < 0.5 * ratio else self.coef[n + 1]
        self.data = new_data
        self.mask = new_mask
        self.coef = new_coef
        self.shape = self.data.shape

    def averaging(self, depth=10):
        self.coef = np.zeros_like(self.data)
        for n in range(self.shape[0]):
            print(f'\rУсреднение: {n + 1} из {self.shape[0]}.', end='')
            matrix = ~self.mask[n].copy()
            matrix = matrix.astype(np.float16)
            for i in np.arange(matrix.shape[0] - 1):
                for j in np.arange(matrix.shape[1] - 1):
                    surround = []
                    for k in np.arange(max(i - depth, 0), min(i + depth + 1, matrix.shape[0])):
                        for l in np.arange(max(j - depth, 0), min(j + depth + 1, matrix.shape[1])):
                            surround.append(matrix[k, l])
                    matrix[i, j] = np.mean(surround)
            self.coef[n] = matrix


if __name__ == "__main__":
    p = Piece()
