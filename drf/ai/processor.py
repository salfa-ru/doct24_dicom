import os
import pickle
import numpy as np
from .data_io import LungsDataLoader
from .model_builder import covid_model
from .patologies import Piece



class LungsAnalyzer(LungsDataLoader):
    def __init__(self, id, segmentation=True):
        super().__init__(id, segmentation)


    def get_mask(self, **kwargs):
        model = kwargs['model']
        path = self.masks_folder + model
        if os.path.exists(path + '.json'):
            mask_json = self.load_mask_json(path + '.json')
            return mask_json
        elif os.path.exists(path + '.nii.gz'):
            mask = self.load_mask(path + '.nii.gz')
        else:
            mask = self.perform_masking(model)
        mask_json = self.mask_to_json(mask, keys=[3])
        self.save_mask_json(mask_json, path + '.json')
        return mask_json

    def perform_masking(self, model='covid'):
        if model == 'covid':
            input_folder = self.data_folder
            index = self.id
            if self.images_meta['type'] == 'dicom':
                self.dicom_to_nifit()
                input_folder = input_folder + index + '/'
                index = 'dicom2nifit'
            nn_model = covid_model(input_folder, self.masks_folder)
            mask = nn_model.predict([index], return_output=True)[0]

            mask = mask.T[:, ::-1, :]
        if not os.path.exists(self.masks_folder):
            os.mkdir(self.masks_folder)
        path = self.masks_folder + model + '.nii.gz'
        self.save_mask(mask, path)
        return mask

    def get_piece_name(self, **kwargs):
        if kwargs['patology'] == 'covid':
            if kwargs['quantity'] == 2:
                return 'cov_deep_r'
            if kwargs['segments'][0] == 1 or kwargs['segments'][0] == 2:
                return 'cov_rt'
            return 'cov_lt'

    def load_piece(self, **kwargs):
        print('Загрузка паталогии.')
        global piece_name
        piece_name = self.get_piece_name(**kwargs)
        path = f'./pieces/{piece_name}.pkl'
        with open(path, 'rb') as f:
            piece = pickle.load(f)
        return piece

    @staticmethod
    def averaging(input_array, depth=1):
        matrix = input_array.copy()
        matrix = matrix.astype(np.float16)
        for i in np.arange(matrix.shape[0] - 1):
            for j in np.arange(matrix.shape[1] - 1):
                surround = []
                for k in np.arange(max(i - depth, 0), min(i + depth + 1, matrix.shape[0])):
                    for l in np.arange(max(j - depth, 0), min(j + depth + 1, matrix.shape[1])):
                        surround.append(matrix[k, l])
                matrix[i, j] = np.mean(surround)
        return matrix

    def get_hight_range(self, segments):
        min_hight = False
        max_hight = False
        for i in range(self.segmentation.shape[0]):
            mask = np.isin(self.segmentation[i], segments)

            if np.count_nonzero(mask) > 10000:
                if not min_hight:
                    min_hight = i
                max_hight = i
        return min_hight, max_hight

    def get_base_point(self, piece, **kwargs):
        print('Поиск базовой точки.', end=' ')
        segments = kwargs['segments']
        min_hight, max_hight = self.get_hight_range(segments)
        start_level = (max_hight - piece.shape[0] + min_hight) // 2
        start_level = start_level * (start_level > 0)
        print(start_level, end=' ')
        idx = min_hight + 3
        lung = []
        if np.any(np.isin(segments, [1, 2])):
            lung.extend([1, 2])
        if np.any(np.isin(segments, [3, 4, 5])):
            lung.extend([3, 4, 5])
        seg_mask = np.ma.masked_where(~np.isin(self.segmentation[idx], lung), self.segmentation[idx])
        seg_cont = self.averaging(~seg_mask.mask)
        seg_cont = np.vectorize(lambda x: 1 if 0.7 < x < 0.95 else 0)(seg_cont)
        seg_cont_points = np.array([(i, j) for i, j in zip(*np.nonzero(seg_cont))])
        if kwargs['quantity'] == 2:
            base_point = (seg_cont_points[:, 0].max(), seg_cont_points[:, 1].min())
            if (base_point[0] - piece.point[0]) < 0 \
                    or (base_point[0] - piece.point[0] + piece.shape[1]) > self.images.shape[1]:
                piece = piece[:, ::-1, :]
                piece.point = (piece.shape[1] - piece.point[0], piece.point[1])
                base_point = (seg_cont_points[:, 0].min(), seg_cont_points[:, 1].min())
            if (base_point[1] - piece.point[1]) < 0 \
                    or (base_point[1] - piece.point[1] + piece.shape[2]) > self.images.shape[2]:
                piece = piece[:, :, ::-1]
                piece.point = (piece.point[0], piece.shape[2] - piece.point[1])
                base_point = (seg_cont_points[:, 0].max(), seg_cont_points[:, 1].max())
        else:
            if piece_name == 'cov_lt':
                av_points = seg_cont_points[seg_cont_points[:, 0] > (seg_cont_points[:, 0].max() - 20)]
            elif piece_name == 'cov_rt':
                av_points = seg_cont_points[seg_cont_points[:, 0] < (seg_cont_points[:, 0].min() + 20)]
            for _ in range(1000):
                i = np.random.randint(len(av_points))
                base_point = av_points[i]
                if base_point[1] > np.median(av_points[:, 1]) // 2:
                    temp_point = (piece.point[0], piece.shape[2] - piece.point[1])
                    if (base_point[0] - temp_point[0]) > 0 and (base_point[1] - temp_point[1]) > 0:
                        piece = piece[:, :, ::-1]
                        piece.point = temp_point
                        break
                if (base_point[0] - piece.point[0]) > 0 and (base_point[1] - piece.point[1]) > 0:
                    break
        print(base_point)
        return base_point, start_level, piece

    def get_generation(self, **kwargs):
        path = self.path + 'generation/'
        if not os.path.exists(path):
            os.mkdir(path)
        gen_keys = ['patology', 'segments', 'quantity', 'size']
        gen_params = [str(kwargs[key]) for key in gen_keys if kwargs[key]]
        gen_name = '_'.join(gen_params)
        path = path + gen_name
        if not os.path.exists(path):
            path = self.perform_generation(gen_name, **kwargs)
        zip_path = path + '.zip'
        if not os.path.exists(zip_path):
            zip_path = self.dicom_to_zip(path)
        return zip_path

    def perform_generation(self, gen_name, **kwargs):
        print('Началась генерация.')
        piece = self.load_piece(**kwargs)
        if self.images.shape[0] > 60:
            ratio = self.images.shape[0] // 50
            piece.scaling(ratio)
        if not self.segmentation:
            self.segmentation = self.load_segmentation()
        seg_mask = ~np.isin(self.segmentation, kwargs.get('segments'))
        seg = np.ma.masked_where(seg_mask, self.segmentation)
        base_point, start_level, piece = self.get_base_point(piece, **kwargs)
        point = (base_point[0] - piece.point[0], base_point[1] - piece.point[1])
        images = self.images.copy()
        for n in range(start_level, start_level + piece.shape[0]):
            print(f'\rГенерация изображений: {n - start_level + 1} из {piece.shape[0]}', end='')
            images[n] = self.insert_piece_on_slide(self.images[n], piece[n - start_level], seg[n], point)
        print('\nСохранение.')
        path = self.path + 'generation/'
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + gen_name
        self.save_to_dicom(images, path)
        return path

    def insert_piece_on_slide(self, base_image, piece, seg, point):
        image = base_image.copy()
        seg_piece_mask = seg.mask[point[0]: point[0] + piece.shape[0], point[1]: point[1] + piece.shape[1]]
        piece_coef = piece.coef.copy()
        piece_coef = piece_coef * ~seg_piece_mask
        # piece_coef = self.averaging(piece_coef * ~seg_piece_mask, depth=1)
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                a = piece_coef[i, j]
                b = 1 - a
                image[point[0] + i, point[1] + j] = a * piece.data[i, j] + b * image[point[0] + i, point[1] + j]
        return image


if __name__ == "__main__":
    l = LungsAnalyzer('0011')
    a = l.get_generation(patology='covid', segments=[5], quantity=1, size=1)
    print(a)
