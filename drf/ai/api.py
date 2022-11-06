import os, shutil

from .processor import LungsAnalyzer
from .patologies import Piece



def api_commander(**kwargs):
    try:
        try:
            analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
        except:
            data_folder = f"./data/{kwargs['id']}/"
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
            os.mkdir(data_folder + 'dicom/')
            # shutil.copy() копируем файлы
            analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
        if kwargs.get('mode') == 'mask':
            return True, analyzer.get_mask(**kwargs)
        elif kwargs.get('mode') == 'gen':
            path = analyzer.get_generation(**kwargs)
            # здесь будет метод для отправки сгенерированного файла в базу
            return True, path
    except Exception as err:
        return False, {'error': str(err)}


if __name__ == "__main__":
    gen_request = {"id": "0001", "mode": "gen", "patology": "covid", "segments": [2], "quantity": 1, 'size': 1}
    mask_request = {"id": "0001", "mode": "mask", "model": "covid"}

    response = api_commander(**mask_request)
    print(response)
    response = api_commander(**gen_request)
    print(response)

