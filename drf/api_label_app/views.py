from http import HTTPStatus

from rest_framework import mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api_label_app.models import Label
from api_label_app.serializers import LabelModelSerializer
from api_research_app.models import Research
from core.pagination import ProjectPagination


class LabelViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        GenericViewSet):
    """
    Объект меток медицинского обследования.

    *
    """

    class Meta:
        ordering = ['-created_at']

    serializer_class = LabelModelSerializer
    permission_classes = (IsAuthenticated,)

    pagination_class = ProjectPagination
    queryset = Label.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['research_id']

    def get_queryset(self):
        return Label.objects.none() if self.request.user.is_anonymous \
            else Label.objects.filter(owner=self.request.user)

    def get_object(self):
        return get_object_or_404(Research,
                                 pk=self.kwargs['pk'],
                                 owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Создание разметки (С АВТОРИЗАЦИЕЙ)

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        label = self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(data={'id': label.id},
                        status=HTTPStatus.CREATED,
                        # headers=headers
                        )

    def perform_create(self, serializer):
        research_id = serializer.initial_data['research_id']
        research = get_object_or_404(Research, pk=research_id)
        return serializer.save(owner=self.request.user, research=research)
