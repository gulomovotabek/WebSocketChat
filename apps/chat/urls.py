from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import ChatViewSet

router = DefaultRouter()
router.register('chat', ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
