from django.db import models

from apps.shared.models import BaseModel


class Message(BaseModel):
    sender = models.ForeignKey('chat.ChatMember', models.CASCADE, related_name='messages')
    text = models.TextField()

    @property
    def chat(self):
        return self.sender.chat

    class Meta:
        ordering = ('-created_time', )
