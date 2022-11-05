from http import HTTPStatus

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

import ai.api as ai
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
        par = serializer.initial_data['data']
        result = ai.api_commander(**par)
        # headers = self.get_success_headers(serializer.data)
        return Response(data=result,
                        status=HTTPStatus.CREATED if result[0] else HTTPStatus.BAD_REQUEST,
                        # headers=headers
                        )
