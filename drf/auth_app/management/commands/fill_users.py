from datetime import datetime
from random import randint
from auth_app.models import User
from core.json import load_from_json, pack_dict
from django.contrib.auth.models import Group

JSON_PATH = 'auth_app/management/json'

def fill():
    """ Фикстура пользователя """

    print('Создание пользователей')
    users = load_from_json(JSON_PATH, 'users')

    for user in users:

        new_user = User(**pack_dict(user))
        new_user.set_password("123")
        new_user.save()
