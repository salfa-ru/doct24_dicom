import base64
import os

import pytest

from django.urls import reverse
from http import HTTPStatus

import constants_auth as const


# @pytest.mark.django_db
# def test_user_phone_verify():
#     UserPhoneVerify.objects.create(phone_number=const.USERNAME, code=const.PHONE_CODE_USER)
#     assert UserPhoneVerify.objects.count() == 1, 'The record was not created in the database'
#
# @pytest.mark.parametrize('phone, status, comment', [(const.USERNAME, HTTPStatus.OK,
#                                                       'the phone number is not valid, the expected status is 400'),
#                                                      ('89999999999', HTTPStatus.BAD_REQUEST,
#                                                      'the phone number is valid, the expected status is 200')])
# @pytest.mark.django_db
# def test_auth_phone_number(phone, status, comment, api_client):
#     url = reverse('auth_phone_number-list')
#     pyload = dict(
#         phone_number=phone
#     )
#     response = api_client.post(url, data=pyload, format='json')
#     assert response.status_code == status, f'{comment}'


@pytest.mark.parametrize('code, status, comment', [(1235, HTTPStatus.FORBIDDEN,
                                                    'the user has login, the expected status is 200'),
                                                   (const.PHONE_CODE_USER, HTTPStatus.OK,
                                                    'the user has not login, the expected status is 403')])
@pytest.mark.django_db
def test_login(code, status, comment, get_phone_number_verify, api_client):
    url = reverse('login_phone_code')
    pyload = dict(
        phone_number=get_phone_number_verify,
        code=code
    )
    if get_phone_number_verify:
        response = api_client.post(url, data=pyload, format='json')
        assert response.status_code == status, f'{comment}'


@pytest.mark.django_db
def test_token_refresh(get_token, api_client):
    url = reverse('token_refresh')
    response = api_client.post(url,
                               data=dict(refresh=get_token['refresh']), format='json')
    assert response.status_code == HTTPStatus.OK, 'Статус 200'


@pytest.mark.parametrize('response_api, phone, status, comment', [(True, const.USERNAME, HTTPStatus.OK,
                                                                   'The entry does not exist in the database'),
                                                                  (False, '+79999999911', HTTPStatus.OK,
                                                                   'The record exists in the database')])
@pytest.mark.django_db
def test_is_phone(response_api, phone, status, comment, get_token, api_client):
    url = reverse('check_phone', args=[phone])
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_token['access'])
    response = api_client.get(url)
    assert response.status_code == status and response_api == response.data['is_phone'], f'{comment}'


@pytest.mark.django_db
def test_create_avatar(get_token, api_client, get_image):
    url = reverse('avatar_user')
    with open(f'{settings.MEDIA_ROOT}/test.jpg', "rb") as img_file:
        image_64_encode = base64.b64encode(img_file.read()).decode('utf-8').strip()
    os.remove(f'{settings.MEDIA_ROOT}/test.jpg')
    avatar = {'file': image_64_encode}
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_token['access'])
    response = api_client.put(url, data=avatar)
    os.remove(f'{settings.MEDIA_ROOT}/{response.data["file"]}')
    assert response.status_code == HTTPStatus.CREATED, 'Статус 400'
