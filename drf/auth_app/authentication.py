import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from config.config import settings as config


def create_access_token(uid):
    return jwt.encode({
        'user_id': uid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            minutes=config.EXPIRES_ACCESS_TOKEN_MINUTES),
        'iat': datetime.datetime.utcnow()
    }, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

        return payload['user_uid']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')


def create_refresh_token(uid):
    return jwt.encode({
        'user_id': uid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=config.EXPIRES_REFRESH_TOKEN_MINUTES),
        'iat': datetime.datetime.utcnow()
    }, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')

        return payload['user_uid']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    """
    Пользовательский класс аутентификации для DRF и JWT
    """

    def authenticate(self, request):

        User = get_user_model()
        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(uid=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        """
        Принудительное выполнение проверки CSRF
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF сбой, сбой с явным сообщением об ошибке
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
