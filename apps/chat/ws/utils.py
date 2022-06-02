from django.db.models import Q

from chat.models import Chat, ChatMember
from shared.consumer import WSMixin
from user.models import User


class ChatWSUtils(WSMixin):

    def get_receiver(self, receiver_id, user_id):
        if not self.is_user_exists(receiver_id):
            return False
        chat = self.get_chat(receiver_id, user_id)
        return {
            'receiver': chat.members.filter(user_id=receiver_id).first(),
            'current_member': chat.members.filter(user_id=user_id).first(),
        }

    @staticmethod
    def is_user_exists(receiver_id):
        if not (type(receiver_id) is int):
            return False
        if not User.objects.filter(id=receiver_id).exists():
            return False
        return True

    def get_chat(self, receiver_id, user_id):
        chats = Chat.objects.filter(members__user_id=receiver_id).filter(members__user_id=user_id)
        if not chats.exists():
            return self.create_chat(receiver_id, user_id)
        return chats.first()

    @staticmethod
    def create_chat(receiver_id, user_id):
        chat = Chat.objects.create()
        ChatMember.objects.bulk_create(
            [
                ChatMember(chat_id=chat.id, user_id=receiver_id),
                ChatMember(chat_id=chat.id, user_id=user_id),
            ]
        )
        return chat
