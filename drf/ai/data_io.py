import os, json, re
import lungmask
import numpy as np
import nibabel as nib
import SimpleITK as sitk
from zipfile import ZipFile
from miscnn.data_loading.interfaces.dicom_io import DICOM_interface
from miscnn.data_loading.interfaces.nifti_io import NIFTI_interface
from dicom2nifti import dicom_series_to_nifti


class LungsDataLoader:
    def __init__(self, id, segmentation=True):
        self.data_folder = './data/'
        self.id = id
        self.path = self.data_folder + self.id + '/'
        self.masks_folder = self.data_folder + self.id + '/masks/'
        if not os.path.exists(self.path):
            raise FileExistsError
        self.interface = self.get_interface()
        if not self.interface:
            raise TypeError
        self.images, self.images_meta = self.load_images()
        self.segmentation = self.load_segmentation() if segmentation else None

    def get_interface(self):
        if os.path.exists(self.path + 'dicom/'):
            for root, _, files in os.walk(self.path + 'dicom/'):
                for f in files:
                    if re.match('.*001.dcm', f):
                        interface = DICOM_interface()
                        interface.initialize(self.path)
                        self.image_index = 'dicom/'
                        return interface
        if os.path.exists(self.path + 'dicom.zip'):
            z = ZipFile(self.path + 'dicom.zip')
            z.extractall(self.path + 'dicom/')
            interface = DICOM_interface()
            interface.initialize(self.path)
            self.image_index = 'dicom/'
            return interface
        if os.path.exists(self.path + 'imaging.nii.gz'):
            interface = NIFTI_interface()
            interface.initialize(self.path)
            self.image_index = ''
            return interface

    def load_images(self):
        images_arr, images_meta = self.interface.load_image(self.image_index)
        if images_meta['type'] == 'nifti':
            images_arr = images_arr[:, ::-1, :]
            images_arr = images_arr.T
        return images_arr, images_meta

    def load_segmentation(self):
        path = self.path + 'segmentation.nii.gz'
        if not os.path.exists(path):
            segmentation = self.perform_segmentation()
            self.save_mask(segmentation, path)
        segmentation = self.load_mask(path)
        return segmentation

    def perform_segmentation(self):
        images = sitk.GetImageFromArray(self.images)
        return lungmask.mask.apply_fused(images)

    def save_mask(self, mask, path):
        mask = nib.Nifti1Image(mask, self.images_meta.get('affine'))
        nib.save(mask, path)

    @staticmethod
    def mask_to_json(mask, keys):
        mask_json = {}
        for n in range(mask.shape[0]):
            zone_dict = {key: [] for key in keys}
            mask_n = mask[n].copy()
            for i in range(mask_n.shape[0]):
                for j in range(mask_n.shape[1]):
                    if mask_n[i, j] in zone_dict.keys():
                        zone_dict[mask_n[i, j]].append((i, j))
            mask_json[n] = zone_dict
        return mask_json

    @staticmethod
    def save_mask_json(mask, path):
        with open(path, 'w') as f:
            json.dump(mask, f)

    @staticmethod
    def load_mask(path):
        return nib.load(path).dataobj

    @staticmethod
    def load_mask_json(path):
        with open(path, 'r') as f:
            return json.load(f)

    def dicom_to_nifit(self):
        dicom_directory = self.path + 'dicom/'
        if not os.path.exists(self.path + 'dicom2nifit/'):
            os.mkdir(self.path + 'dicom2nifit/')
        elif os.path.exists(self.path + 'dicom2nifit/imaging.nii.gz'):
            return
        output_file = self.path + 'dicom2nifit/imaging.nii.gz'
        dicom_series_to_nifti(dicom_directory, output_file, reorient_nifti=True)

    @staticmethod
    def save_to_dicom(array, path):
        if not os.path.exists(path):
            os.mkdir(path)
        array = array.astype(np.int16)
        for n in range(array.shape[0]):
            img = sitk.GetImageFromArray(array[n])
            sitk.WriteImage(img, f'{path}/{n + 1:04}.dcm')


if __name__ == "__main__":
    pass
