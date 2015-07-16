import tgbot


class SimsimiPlugin(tgbot.TGPluginBase):
    def simsimi(self, bot, message, text):
        import requests

        res = requests.get('http://www.simsimi.com/requestChat', params={
            'lc': 'en',
            'ft': '1.0',
            'req': text,
        }).json()

        bot.tg.send_message(message.chat.id, res['res'])

    def chat(self, bot, message, text):
        return self.simsimi(bot, message, text)
