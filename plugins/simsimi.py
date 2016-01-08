import tgbot
from twx.botapi import ChatAction
import requests


class SimsimiPlugin(tgbot.TGPluginBase):
    def simsimi(self, message, text):
        self.bot.send_chat_action(message.chat.id, ChatAction.TEXT)

        res = requests.get('http://www.simsimi.com/requestChat', params={
            'lc': 'en',
            'ft': '1.0',
            'req': text,
        }).json()

        self.bot.send_message(message.chat.id, res['res'])

    def chat(self, message, text):
        return self.simsimi(message, text)
