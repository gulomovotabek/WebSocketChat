from django.db.models import Q
from rest_framework import serializers

from chat.models import Chat, ChatMember


class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = (
            'id',
            'user',
        )


class ChatSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            'id',
            'member',
        )

    def get_member(self, obj):
        return ChatMemberSerializer(
            obj.members.filter(~Q(user_id=self.context['request'].user.id)).first(),
            context=self.context,
        ).data
