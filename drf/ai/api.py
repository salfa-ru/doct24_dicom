import os, shutil
from .processor import LungsAnalyzer


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
            return True, analyzer.get_mask(kwargs['model'])
        elif kwargs.get('mode') == 'gen':
            path = analyzer.get_generation(**kwargs)
            #здесь будет метод для отправки сгенерированного файла в базу
            return True, path
    except Exception as err:
        return False, {'error': str(err)}
