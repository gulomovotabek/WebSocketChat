from django.db import models
from django.db.models import Q
from django.db.transaction import atomic

from shared.models import BaseModel


class Chat(BaseModel):
    """
    One to one chat between two user
    """
    pass


class ChatMember(BaseModel):
    chat = models.ForeignKey('chat.Chat', models.CASCADE, related_name='members')
    user = models.ForeignKey('user.User', models.CASCADE, related_name='members')

    @property
    def opposite_member(self):
        return self.chat.members.filter(~Q(id=self.id)).first()

    @atomic
    def delete(self, **kwargs):
        self.chat.delete()
        return super(ChatMember, self).delete(**kwargs)
