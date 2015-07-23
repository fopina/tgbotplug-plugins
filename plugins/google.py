import tgbot
import re
import HTMLParser
from twx.botapi import ForceReply


class GooglePlugin(tgbot.TGPluginBase):
    TAG_RE = re.compile(r'<[^>]+>')

    def __init__(self):
        super(GooglePlugin, self).__init__()
        self.unescaper = HTMLParser.HTMLParser()

    def list_commands(self):
        return [
            ('g', self.google, 'Google this')
        ]

    def google(self, bot, message, text):
        if not text:
            m = bot.tg.send_message(
                message.chat.id,
                'Google for what?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(selective=True)
            ).wait()
            self.need_reply(self.google, message, out_message=m, selective=True)
        else:
            import requests

            res = requests.get('http://ajax.googleapis.com/ajax/services/search/web', params={
                'v': 1.0,
                'q': text,
            }).json()

            if res['responseStatus'] == 200:
                try:
                    res = res['responseData']['results'][0]
                    res['content'] = self.unescaper.unescape(GooglePlugin.TAG_RE.sub('',  res['content']))
                    reply = '%(titleNoFormatting)s\n\n%(content)s\n\n%(url)s' % res
                except IndexError:
                    reply = 'Sorry, nothing found...'
            else:
                reply = 'It seems I\'m googling too much lately, I need to rest a little...'

            bot.tg.send_message(message.chat.id, reply, reply_to_message_id=message.message_id)
