from django.db import models

class Label(models.Model):

    class Meta:
        verbose_name_plural = 'метки врача'
        verbose_name = 'метки врача'

    research = models.ForeignKey(
        "api_research_app.Research",
        verbose_name='исследование',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        "auth_app.User",
        verbose_name='владелец',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    labels = models.JSONField(verbose_name="данные меток врача",
                              blank=True,
                              null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='время обновления')

