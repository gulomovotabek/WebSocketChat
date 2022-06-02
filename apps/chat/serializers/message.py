from rest_framework import serializers

from chat.models import Message
from chat.serializers.chat import ChatMemberSerializer


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'text',
        )

    def to_representation(self, instance):
        data = super(MessageCreateSerializer, self).to_representation(instance)
        data['chat_id'] = instance.chat.id
        data['sender'] = ChatMemberSerializer(instance.sender).data
        return data


class MessageListSerializer(serializers.ModelSerializer):
    sender = ChatMemberSerializer()

    class Meta:
        model = Message
        fields = (
            'id',
            'text',
            'sender',
            'created_time',
        )
