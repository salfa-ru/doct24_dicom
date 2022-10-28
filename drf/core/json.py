import json
import os


def load_from_json(json_path, file_name):
    """ Загрузка файла с словарь """
    with open(
            os.path.join(
                json_path,
                file_name + '.json'),
            'r',
            encoding='utf-8') as infile:
        return json.load(infile)


def pack_dict(dict_pack: dict):
    """ Упаковка словаря """
    return {key: value for key, value in dict_pack.items() if value}
