from rest_framework import mixins, viewsets, filters
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated

from api_research_app.models import Research
from api_research_app.serializers import ResearchModelSerializer
from core.pagination import ProjectPagination


class ResearchViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """
    Обновление файла авторизованного пользователя.

    *Обновление файла авторизованного пользователя.
    """

    class Meta:
        ordering = ['-created_at']

    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    pagination_class = ProjectPagination
    serializer_class = ResearchModelSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Research.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient_code', ]

    # def get_object(self):
    #     return get_object_or_404(Research,
    #                             pk=self.kwargs['pk'],
    #                             owner=self.request.user)

    # def create(self, request, *args, **kwargs):
    #
    #
    #     # serializer = self.get_serializer(data=request.data)
    #     # try:
    #     #     serializer.is_valid(raise_exception=True)
    #     #     self.perform_create(serializer)
    #     # except Exception as err:
    #     return Response(status=HTTPStatus.OK, data=123)
    #     # return super(ResearchViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Получение списка файлов авторизованного пользователя

        *Получение списка файлов авторизованного пользователя

        """

        return super(ResearchViewSet, self).list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Получение ссылки на файл по id авторизованного пользователя

        *Получение ссылки на файл по id авторизованного пользователя

        """

        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Обновление файла по id авторизованного пользователя

        *Обновление файла по id авторизованного пользователя

        """
        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление файла по id авторизованного пользователя

        *Удаление файла по id авторизованного пользователя

        """
        return super().destroy(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """
        Загрузка файла по авторизованному пользователю

        *Загрузка файла по авторизованному пользователю

        """
        return super().create(request, args, kwargs)
