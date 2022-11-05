from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(ModelSerializer):

    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = (
            'uuid',
            'first_name',
            'last_name',
            'patronymic',
        )
