from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_research_app.views import ResearchViewSet

router = DefaultRouter()
router.register('research', ResearchViewSet, basename='research')

urlpatterns = [
    path('v1/', include(router.urls)),
]
