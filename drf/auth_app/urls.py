from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from auth_app.views import UserModelViewSet

urlpatterns = [

    path('v1/authentification/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/authentification/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/user/me/',
         UserModelViewSet.as_view(
             {'get': 'get_user',
              # 'post': 'update_user',
              }),
         name='me'),
]
