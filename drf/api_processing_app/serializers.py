from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_label_app.models import Label


class ProcessingSerializer(ModelSerializer):
    """ Сериализатор процесса  """

    data = serializers.JSONField(write_only=True, source=None)

    class Meta:
        model = Label
        fields = ['data']
