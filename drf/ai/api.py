import os, shutil, requests, json
from .processor import LungsAnalyzer
from .patologies import Piece


username = 'admin'
password = 'admin'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NTQyNDA3LCJpYXQiOjE2Njg0NTYwMDcsImp0aSI6ImVmZjJmMmE4YjNkODQ5MjZiYjMwNjY4MWVhYjAxMjIwIiwidXNlcl9pZCI6ImFiZjc3YWUwLTE0NGMtNDYwNy05MGFlLWJlZTU1MGM5ZGRmNiJ9.Kxcupf8ffrFYYNeZP9SX4aEqifOwkozf0ZreuEfqiwk'

def api_commander(**kwargs):

    print('НАЧАЛО-',kwargs)
    #token= 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NTI4Mzg5LCJpYXQiOjE2Njg0NDE5ODksImp0aSI6IjQ3ZDViZjVhNGU5MTRiYjliODY1ZDgwYWZkMzc3ODVjIiwidXNlcl9pZCI6IjIwOGQyMTk5LTNkYmMtNDVhMy1iOTY3LWY2OWZlY2Y1ZjkwMiJ9.B2hMgFHTQc7VI7jGGl2dyUVEd4hz-mLkN4AEjlSLL0Q'

    #try:
    print(kwargs)
    print('текущий каталог:',os.getcwd())
    try:
        analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
    except:
        print(os.listdir())
        print('Создание каталога')
        data_folder = f"/home/app/web/ai/data/{kwargs['id']}/"
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        path = get_media_path(kwargs['id'])
        print(path)
        if not path.split(".")[-1] == 'zip':
            data_folder = data_folder + 'dicom/'
            os.mkdir(data_folder)
        shutil.copy(path, data_folder)
        analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
    if kwargs.get('mode') == 'mask':
        mask = analyzer.get_mask(**kwargs)
        send_mask_to_base(analyzer.id, mask)
        return True, mask
    elif kwargs.get('mode') == 'gen':
        print('ЗАХОД GEN')
        path = analyzer.get_generation(**kwargs)
        print('ПОЛУЧЕНИЕ ПУТИ')
        filename = "_".join([kwargs['id'], kwargs['mode'], kwargs['patology']])
        send_gen_to_base(filename, path)
        return True, path
    #except Exception as err:
    #    return False, {'error': str(err)}


def send_gen_to_base(filename, path):
    url = "http://92.255.110.75:8000/api/v1/research/"
    payload = {'patient_code': 'AUTO'}
    files = [
        ('media_file', (filename, open(path, 'rb'), 'application/octet-stream'))]
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)


def update_token():
    '''
    curl -X 'POST' \
      'http://92.255.110.75:8000/api/v1/authentification/token/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "username": "admin",
      "password": "admin"
    }'
    '''
    
    print('получаем токен')
    url = "http://92.255.110.75:8000/api/v1/authentification/token/"
    payload = json.dumps({"username": username, "password": password})
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    tt = json.loads(response.text)
    return tt['access']


def send_mask_to_base(id, mask):
    print('передаём файл')
    url = "http://92.255.110.75:8000/api/v1/labels/"
    payload = json.dumps({"research_id": id, "labels": mask})
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def get_media_path(id):
    '''
      curl -X 'GET' \
           'http://92.255.110.75:8000/api/v1/research/16/' \
           -H 'accept: application/json' \
           -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NTMzMTIzLCJpYXQiOjE2Njg0NDY3MjMsImp0aSI6ImRlODYyOGZkNWFkZjQ5NTViMjExYThmNTdlZDZhZDU4IiwidXNlcl9pZCI6IjIwOGQyMTk5LTNkYmMtNDVhMy1iOTY3LWY2OWZlY2Y1ZjkwMiJ9.QchwNXC6lPZV1vG2l0V0QmZfdIRyCRWJEs2Gx1QqPfw'
    '''
    print('получаем файл')
    url = f"http://92.255.110.75:8000/api/v1/research/{id}/"
    print(url)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    print(headers)
    response = None
    try:
        response = requests.request("GET", url, headers=headers)
    except BaseException as err:
        print(err)
    print('после трай', response)
    response = response.json()
    print(response)
    path = response["media_file"]
    path = "/media" + path.split('media')[-1]
    return path


if __name__ == "__main__":
    gen_request = {"id": "0009", "mode": "gen", "patology": "covid", "segments": [5], "quantity": 1,
                   'size': 1}
    mask_request = {"id": "0008", "mode": "mask", "model": "covid"}

    request = {"id": "1"}

    # response = api_commander(**mask_request)
    # print(response)
    response = api_commander(**gen_request)
    print(response)
    # response = api_commander(**request)
    # print(response)
