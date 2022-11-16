from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from api_label_app.models import Label


class ProcessingSerializer(Serializer):
    """ Сериализатор процесса  """

    data = serializers.JSONField(write_only=True)
    #
    # class Meta:
    #     # model = Label
    #     fields = ['data']
