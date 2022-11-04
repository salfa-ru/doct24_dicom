from http import HTTPStatus

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import ProcessingSerializer


class ProcessingViewSet(
        mixins.CreateModelMixin,
        GenericViewSet):
    """
    Объект меток медицинского обследования.

    *

    """

    permission_classes = (IsAuthenticated,)

    pagination_class = None
    serializer_class = ProcessingSerializer

    def create(self, request, *args, **kwargs):
        """
        Создание разметки (С АВТОРИЗАЦИЕЙ)

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = "Результат"
        # headers = self.get_success_headers(serializer.data)
        return Response(data=result,
                        status=HTTPStatus.CREATED,
                        # headers=headers
                        )
