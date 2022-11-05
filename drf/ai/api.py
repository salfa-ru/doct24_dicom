import os, shutil, requests, json
from processor import LungsAnalyzer
from patologies import Piece


def api_commander(**kwargs):
    try:
        try:
            analyzer = LungsAnalyzer(kwargs['id'], segmentation=True)
        except:
            data_folder = f"./data/{kwargs['id']}/"
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
            path = get_media_path(kwargs['id'])
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
            path = analyzer.get_generation(**kwargs)
            filename = "_".join([kwargs['id'], kwargs['mode'], kwargs['patology']])
            send_gen_to_base(filename, path)
            return True, path
    except Exception as err:
        return False, {'error': str(err)}


def send_gen_to_base(filename, path):
    url = "http://92.255.110.75:8000/api/v1/research/"
    payload = {'patient_code': 'AUTO'}
    files = [
        ('media_file', (filename, open(path, 'rb'), 'application/octet-stream'))]
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NzUxMTMyLCJpYXQiOjE2Njc2NjQ3MzIsImp0aSI6IjhkMDNiZGZkMWE3ZjQwMzViNmM4N2E2NGNkMTEzOGZlIiwidXNlcl9pZCI6ImI2ODQ4ODg4LTNlNmYtNDUyNy05ZGE3LTdiMWVmNjQxMDc3ZiJ9.F2BKil2JpqSscIEr0ByVBDCLIDQEyDmeXKpUTnnpkXs'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)


def send_mask_to_base(id, mask):
    url = "http://92.255.110.75:8000/api/v1/labels/"
    payload = json.dumps({"research_id": id, "labels": mask})
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NzUxMTMyLCJpYXQiOjE2Njc2NjQ3MzIsImp0aSI6IjhkMDNiZGZkMWE3ZjQwMzViNmM4N2E2NGNkMTEzOGZlIiwidXNlcl9pZCI6ImI2ODQ4ODg4LTNlNmYtNDUyNy05ZGE3LTdiMWVmNjQxMDc3ZiJ9.F2BKil2JpqSscIEr0ByVBDCLIDQEyDmeXKpUTnnpkXs'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def get_media_path(id):
    url = f"http://92.255.110.75:8000/api/v1/research/{id}/"
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NzUxMTMyLCJpYXQiOjE2Njc2NjQ3MzIsImp0aSI6IjhkMDNiZGZkMWE3ZjQwMzViNmM4N2E2NGNkMTEzOGZlIiwidXNlcl9pZCI6ImI2ODQ4ODg4LTNlNmYtNDUyNy05ZGE3LTdiMWVmNjQxMDc3ZiJ9.F2BKil2JpqSscIEr0ByVBDCLIDQEyDmeXKpUTnnpkXs'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    response = response.json()
    path = response["media_file"]
    path = "/media" + path.split('media')[-1]
    return path

if __name__ == "__main__":
    gen_request = {"id": "0001", "mode": "gen", "patology": "covid", "segments": [1, 2, 3, 4, 5], "quantity": 2,
                   'size': 1}
    mask_request = {"id": "0001", "mode": "mask", "model": "covid"}

    request = {"id": "1"}

    # response = api_commander(**mask_request)
    # print(response)
    response = api_commander(**gen_request)
    print(response)
    # response = api_commander(**request)
    # print(response)
