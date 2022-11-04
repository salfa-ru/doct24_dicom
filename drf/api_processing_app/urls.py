from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_processing_app.views import ProcessingViewSet

router = DefaultRouter()
router.register('ai/processing', ProcessingViewSet, basename='ai_processing')

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/processing/', ProcessingViewSet.as_view, name='run_processing')
]
