from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
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
    Частичное обновление разметки авторизованного пользователя.

    *Частичное обновление разметки авторизованного пользователя.
    """

    class Meta:
        ordering = ['-created_at']

    serializer_class = LabelModelSerializer
    permission_classes = (IsAuthenticated,)

    pagination_class = ProjectPagination
    queryset = Label.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['research__id']

    def get_queryset(self):
        return Label.objects.none() if self.request.user.is_anonymous \
            else Label.objects.filter(owner=self.request.user)

    # def get_object(self):
    #     return get_object_or_404(Research,
    #                              pk=self.kwargs['pk'],
    #                              owner=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Получение список разметок авторизованного пользователя

        *Получение список разметок авторизованного пользователя

        """
        return super(LabelViewSet, self).list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Получение разметки по id авторизованного пользователя

        *Получение разметки по id авторизованного пользователя

        """
        return super(LabelViewSet, self).retrieve(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        """
        Обновление разметки по id авторизованного пользователя

        *Обновление разметки по id авторизованного пользователя

        """
        return super(LabelViewSet, self).update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление разметки по id авторизованного пользователя

        *Удаление разметки по id авторизованного пользователя

        """
        return super(LabelViewSet, self).destroy(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создание разметки по авторизованному пользователю

        *Создание разметки по авторизованному пользователю

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
        """
        Обновление разметки по id авторизованного пользователя

        *Обновление разметки по id авторизованного пользователя

        """
        research_id = serializer.initial_data['research_id']
        research = get_object_or_404(Research, pk=research_id)
        return serializer.save(owner=self.request.user, research=research)
