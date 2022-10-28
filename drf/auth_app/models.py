from datetime import datetime
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models


# Модель пользователя
class User(AbstractUser):
    """ Модель пользователя """

    class Meta:
        verbose_name_plural = 'пользователи системы'
        verbose_name = 'пользователь системы'

    uid = models.UUIDField(verbose_name='ид', primary_key=True, default=uuid4)
    username = models.CharField(verbose_name='имя пользователя',
                                max_length=250, unique=True)
    patronymic = models.CharField(verbose_name='отчество', max_length=250,
                                  null=True, blank=True, default='')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='время обновления')
    deleted_at = models.DateTimeField(
        verbose_name='время удаления',
        null=True, blank=True
    )
    is_delete = models.BooleanField(default=False, verbose_name='удален')

    def delete(self, **kwargs):
        """
        :return: переопределяем метода удаления записи
        """
        self.is_delete = True
        self.deleted_at = datetime.now()
        self.save()

    def __str__(self):
        """
        :return: переопределение представление
        """
        return f'{self.first_name if self.first_name else ""} ' \
               f'{self.patronymic if self.patronymic else ""} ' \
               f'{self.last_name if self.last_name else ""} '
