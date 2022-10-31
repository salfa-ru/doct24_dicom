from rest_framework import mixins, viewsets, filters
from rest_framework.generics import get_object_or_404
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
    Объект медицинского обследования.

    Использовать формат BASE64 для media_file.

    *
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

    def get_object(self):
        return get_object_or_404(Research,
                                pk=self.kwargs['pk'],
                                owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



