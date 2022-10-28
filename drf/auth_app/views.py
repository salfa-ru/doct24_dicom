from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserModelViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    Работа с моделью пользователей

    *
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_user(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def update_user(self, request):
        instance = User.objects.get(uid=request.user.uid)
        serializer = self.serializer_class(
            data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
