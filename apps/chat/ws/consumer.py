import json

from chat.ws.actions import ChatWSActions
from core.const.ws import MAIN_SCOPE


class ChatConsumer(ChatWSActions):
    CHANNEL_NAME = MAIN_SCOPE

    def socket_action(self, action, data):
        if self.get_item_by_index(action, 0) == 'chat':

            if self.get_item_by_index(action, 1) == 'send_message':
                ret_data = self.send_message(data, '.'.join(action))
                if ret_data:
                    self.send(text_data=json.dumps(ret_data, ensure_ascii=False))
                    return

            """
            so now, here, can write any chat actions like delete message, open group and etc
            """

        ret_data = self.no_action_found()
        self.send(text_data=json.dumps(ret_data, ensure_ascii=False))
        return
