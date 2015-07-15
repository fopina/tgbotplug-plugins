import tgbot
import re
from twx.botapi import ForceReply


class GooglePlugin(tgbot.TGPluginBase):
    TAG_RE = re.compile(r'<[^>]+>')

    def list_commands(self):
        return [
            ('g', self.google, 'Google this')
        ]

    def google(self, tg, message, text):
        if not text:
            tg.send_message(message.chat.id, 'Google for what?', reply_to_message_id=message.message_id, reply_markup=ForceReply.create(selective=True))
            return

        import requests

        res = requests.get('http://ajax.googleapis.com/ajax/services/search/web', params={
            'v': 1.0,
            'q': text,
        }).json()['responseData']['results'][0]

        res['content'] = GooglePlugin.TAG_RE.sub('', res['content'])
        reply = '''\
%(titleNoFormatting)s

%(content)s

%(url)s\
''' % res

        tg.send_message(message.chat.id, reply)
