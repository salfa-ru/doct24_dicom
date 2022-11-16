import logging

import os
import shutil
import requests
import json
from .processor import LungsAnalyzer
from .patologies import Piece

host = 'localhost:8000'
username = 'admin'
password = 'admin'
token = None


def api_commander(**kwargs):

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logging.info(f'{"*"*10}Начало{"*"*10}')
    logging.info(f'параметры{kwargs}')

    try:
        analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
    except Exception as err:
        logging.warning(f'ошибка:{err}')
        data_folder = f"./ai/data/{kwargs['id']}/"
        if not os.path.exists(data_folder):
            logging.info(f'Создание каталога: {data_folder}')
            os.mkdir(data_folder)
        _path = get_media_path(kwargs['id'])
        logging.info(f'Локальный путь{_path}')
        if not _path.split(".")[-1] == 'zip':
            data_folder = data_folder + 'dicom/'
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
        basename = os.path.basename(_path)

        if basename.split('.')[-1].lower() == 'dcm':
            new_path = os.path.join(data_folder, '0001.' +
                                    basename.split('.')[1])
        elif basename.split('.')[-1].lower() == 'zip':
            new_path = os.path.join(data_folder, 'dicom.zip')
        else:
            new_path = data_folder

        shutil.copy2(_path, new_path)

        analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
    if kwargs.get('mode') == 'mask':
        mask = analyzer.get_mask(**kwargs)
        send_mask_to_base(analyzer.id, mask)
        return True, mask
    elif kwargs.get('mode') == 'gen':
        print('ЗАХОД GEN')
        _path = analyzer.get_generation(**kwargs)
        print('ПОЛУЧЕНИЕ ПУТИ')
        filename = "_".join(
            [str(kwargs['id']), kwargs['mode'], kwargs['patology']]) + '.zip'
        send_gen_to_base(filename, _path)
        return True, _path
    # except Exception as err:
    #    return False, {'error': str(err)}


def send_gen_to_base(filename, path):

    token = update_token()
    url = f'http://{host}/api/v1/research/'
    payload = {'patient_code': 'AUTO'}
    files = [
        ('media_file',
         (filename,
          open(
              path,
              'rb'),
             'application/octet-stream'))]
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        files=files)
    print(response.text)


def update_token():
    """
    curl -X 'POST' \
      'http://92.255.110.75:8000/api/v1/authentification/token/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "username": "admin",
      "password": "admin"
    }'
    """

    logging.info('получаем токен')
    url = f'http://{host}/api/v1/authentification/token/'
    payload = json.dumps(
        {"username": username,
         "password": password}
    )
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    try:
        res = requests.request("POST", url, headers=headers, data=payload)
    except Exception as err:
        logging.info(str(err))
        return
    tt = json.loads(res.text)
    logging.info(tt['access'])
    return tt['access']


def send_mask_to_base(id, mask):

    token = update_token()
    print('передаём файл')
    url = f"http://{host}/api/v1/labels/"
    payload = json.dumps({"research_id": id, "labels": mask})
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def get_media_path(id):
    """
      curl -X 'GET' \
           'http://92.255.110.75:8000/api/v1/research/16/' \
           -H 'accept: application/json' \
           -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NTMzMTIzLCJpYXQiOjE2Njg0NDY3MjMsImp0aSI6ImRlODYyOGZkNWFkZjQ5NTViMjExYThmNTdlZDZhZDU4IiwidXNlcl9pZCI6IjIwOGQyMTk5LTNkYmMtNDVhMy1iOTY3LWY2OWZlY2Y1ZjkwMiJ9.QchwNXC6lPZV1vG2l0V0QmZfdIRyCRWJEs2Gx1QqPfw'
    """
    token = update_token()
    logging.info('получаем файл')
    url = f"http://{host}/api/v1/research/{id}/"
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    response = None
    try:
        res = requests.request("GET", url, headers=headers)
    except Exception as err:
        logging.fatal(str(err))
        return None

    tt = json.loads(res.text)
    path = tt["media_file"]
    path = "./media" + path.split('media')[-1]
    # if not os.path.exists(path):
    path = os.path.join('/home/app/web/media', path.split("media")[-1])
    logging.info(path)
    return path


if __name__ == "__main__":
    gen_request = {
        "id": "0009",
        "mode": "gen",
        "patology": "covid",
        "segments": [5],
        "quantity": 1,
        'size': 1}
    mask_request = {"id": "0008", "mode": "mask", "model": "covid"}

    request = {"id": "1"}

    # response = api_commander(**mask_request)
    # print(response)
    response = api_commander(**gen_request)
    print(response)
    # response = api_commander(**request)
    # print(response)
