from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from chat.models import Message
from chat.serializers import MessageListSerializer


class MessageListViewSet(ListModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
