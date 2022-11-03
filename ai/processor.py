import os
from data_io import LungsDataLoader
from model_builder import covid_model


class LungsAnalyzer(LungsDataLoader):
    def __init__(self, id, segmentation=True):
        super().__init__(id, segmentation)

    def insert_piece(self, lungs_zone=5):
        pass

    def get_mask(self, model='covid'):
        path = self.masks_folder + model + '.nii.gz'
        if os.path.exists(path):
            mask = self.load_mask(path)
            return mask
        if model == 'covid':
            input_folder = self.data_folder
            index = self.id
            if self.images_meta['type'] == 'dicom':
                self.dicom_to_nifit()
                input_folder = input_folder + index + '/'
                index = 'dicom2nifit'
            model = covid_model(input_folder, self.masks_folder)
            mask = model.predict([index], return_output=True)[0]
            mask = mask.T[:, ::-1, :]
            if not os.path.exists(self.masks_folder):
                os.mkdir(self.masks_folder)
            self.save_mask(mask, path)
        return mask


if __name__ == "__main__":
    pass
