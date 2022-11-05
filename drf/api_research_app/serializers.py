from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_research_app.models import Research
from auth_app.serializers import UserSerializer
from core.serializer import TimestampField


class ResearchModelSerializer(ModelSerializer):
    """ Сериализатор медицинского исследования """

    id = serializers.IntegerField(read_only=True)
    media_file = serializers.FileField(required=True)
    patient_code = serializers.CharField(required=False)
    owner = UserSerializer(read_only=True)
    created_at = TimestampField(read_only=True)
    updated_at = TimestampField(read_only=True)

    class Meta:
        model = Research
        fields = (
            'id',
            'patient_code',
            'owner',
            'media_file',
            'created_at',
            'updated_at'
        )
