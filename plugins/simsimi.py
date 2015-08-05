import tgbot
from twx.botapi import ChatAction
import requests


class SimsimiPlugin(tgbot.TGPluginBase):
    def simsimi(self, bot, message, text):
        bot.send_chat_action(message.chat.id, ChatAction.TEXT)

        res = requests.get('http://www.simsimi.com/requestChat', params={
            'lc': 'en',
            'ft': '1.0',
            'req': text,
        }).json()

        bot.send_message(message.chat.id, res['res'])

    def chat(self, bot, message, text):
        return self.simsimi(bot, message, text)
