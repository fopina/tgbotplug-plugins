import tgbot


class SimsimiPlugin(tgbot.TGPluginBase):
    def simsimi(self, tg, message, text):
        import requests

        res = requests.get('http://www.simsimi.com/requestChat', params={
            'lc': 'en',
            'ft': '1.0',
            'req': text,
        }).json()

        tg.send_message(message.chat.id, res['res'])
