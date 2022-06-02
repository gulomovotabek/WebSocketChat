from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageListSerializer
from shared.pagination import DefaultPagination


class ChatViewSet(ListModelMixin, GenericViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return self.queryset.filter(members__user_id=self.request.user.id)

    @action(['GET'], True, serializer_class=MessageListSerializer)
    def messages(self, request, pk, *args, **kwargs):
        messages = Message.objects.filter(sender__chat_id=pk)
        page = self.paginate_queryset(messages)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
