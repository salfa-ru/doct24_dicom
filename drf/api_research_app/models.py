from django.db import models
from auth_app.models import User


class Research(models.Model):
    """ Основная модель хранения данных по исследованию """

    class Meta:
        verbose_name_plural = 'исследования'
        verbose_name = 'иследование'

    patient_code = models.CharField(
        verbose_name='внешний ключ пациента',
        max_length=25,
        blank=True,
        default='')
    media_file = models.FileField(
        verbose_name='файл',
        upload_to='',
        blank=True)
    owner = models.ForeignKey(
        User,
        verbose_name='владелец',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='время обновления')
