from rest_framework.serializers import ModelSerializer

from core.serializer import TimestampField
from .models import User


class UserMiniModelSerializer(ModelSerializer):
    """ Serializer пользователей для модели пациенты  """

    class Meta:
        model = User
        fields = ('uid', 'first_name', 'last_name', 'patronymic')


class UserShortModelSerializer(ModelSerializer):
    """ Serializer пользователей для модели пациенты  """
    birthday = TimestampField(required=False)

    class Meta:
        model = User
        fields = ('uid', 'first_name', 'last_name', 'patronymic')


class PostUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            # 'uid',
            'first_name',
            'last_name',
            'patronymic',
        )

    def create(self, validated_data):
        instance = User.objects.update_or_create(
            pk=self.context['pk'], defaults=validated_data)
        return instance

    def update(self, instance, validated_data):

        if 'first_name' in validated_data:
            instance.first_name = validated_data.get(
                'first_name', instance.first_name)

        if 'last_name' in validated_data:
            instance.last_name = validated_data.get(
                'last_name', instance.last_name)

        if 'patronymic' in validated_data:
            instance.patronymic = validated_data.get(
                'patronymic', instance.patronymic)

        instance.save()
        return instance


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
        )
