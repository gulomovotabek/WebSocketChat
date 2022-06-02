from chat.serializers import MessageCreateSerializer
from chat.ws.utils import ChatWSUtils
from core.const.ws import MAIN_SCOPE


class ChatWSActions(ChatWSUtils):

    def send_message(self, data, action):
        members = self.get_receiver(data.get('receiver_id'), self.scope['user'].id)
        if not (type(members) is dict):
            return False
        serializer = MessageCreateSerializer(data=data)
        if not serializer.is_valid():
            return False
        serializer.save(sender_id=members['current_member'].id)
        ret_data = {
            "is_success": True,
            "action": action,
            "message": 'new personal message',
            "data": serializer.data,
        }
        self.send_data_to_user(
            MAIN_SCOPE,
            members['receiver'].user_id,
            json_data=ret_data
        )
        return ret_data
