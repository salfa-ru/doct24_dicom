import pytest
from auth_app.models import UserPhoneVerify, User
from django.urls import reverse
from PIL import Image

import constants_auth as const
from doct24 import settings


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_user():
    """Фикстура юзера для пациента."""
    User.objects.create(username=const.USERNAME, phone=const.USERNAME)
    return User.objects.get(username=const.USERNAME)


@pytest.fixture
def get_phone_number_verify():
    """Фикстура верифицированного телефона"""
    phone_verify = UserPhoneVerify.objects.create(phone_number=const.USERNAME, code=const.PHONE_CODE_USER)
    return phone_verify.phone_number


@pytest.fixture
@pytest.mark.django_db
def get_token(get_phone_number_verify, api_client):
    """Фикстура токена пользователя"""
    url = reverse('login_phone_code')
    pyload = dict(
        phone_number=get_phone_number_verify,
        code=const.PHONE_CODE_USER
    )
    if get_phone_number_verify:
        response = api_client.post(url, data=pyload, format='json')
        return response.data


@pytest.fixture
def get_image():
    img = Image.new('RGB', (200, 200), 'black')
    img.save(fp=f'{settings.MEDIA_ROOT}/test.jpg')
    return img
