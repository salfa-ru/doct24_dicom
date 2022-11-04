from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api_label_app.models import Label
from api_research_app.models import Research
from api_research_app.serializers import ResearchModelSerializer
from auth_app.serializers import UserSerializer
from core.serializer import TimestampField


class LabelModelSerializer(ModelSerializer):
    """ Сериализатор медицинского исследования """

    id = serializers.IntegerField(read_only=True)
    research_id = serializers.IntegerField(required=True)
    labels = serializers.JSONField(required=True)
    created_at = TimestampField(read_only=True)
    updated_at = TimestampField(read_only=True)

    class Meta:
        model = Label
        fields = (
            'id',
            'research_id',
            'labels',
            'created_at',
            'updated_at'
        )

    def validate(self, attrs):
        if not Research.objects.filter(pk=self.initial_data['research_id']):
            raise serializers.ValidationError(
                "не найдено медицинское обследование"
            )
        return super(LabelModelSerializer, self).validate(attrs)

