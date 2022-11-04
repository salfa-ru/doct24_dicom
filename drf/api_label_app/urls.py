from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_label_app.views import LabelViewSet

router = DefaultRouter()
router.register('labels', LabelViewSet, basename='labels')

urlpatterns = [
    path('v1/', include(router.urls)),
]
