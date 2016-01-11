# coding=utf-8
from tgbot import plugintest
from tgbot.botapi import Update
from plugins.google import GooglePlugin

from requests.packages import urllib3
urllib3.disable_warnings()


class GooglePluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[GooglePlugin()])
        self.received_id = 1

    def receive_message(self, text, sender=None, chat=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        if chat is None:
            chat = sender

        self.bot.process_update(
            Update.from_dict({
                'update_id': self.received_id,
                'message': {
                    'message_id': self.received_id,
                    'text': text,
                    'chat': chat,
                    'from': sender,
                }
            })
        )

        self.received_id += 1

    def test_not_found(self):
        self.receive_message('/g site:www.android.com "iphone is awesome"')
        self.assertReplied(self.bot, 'Sorry, nothing found...')

    def test_reply(self):
        self.receive_message('/g site:skmobi.com TimeIsMoney')
        self.assertReplied(self.bot, u'''\
skmobi - TimeIsMoney

Time is Money! So, "time" your money with this app. TimeIsMoney uses the \n\
interface you're used to from Clock.app stopwatch, but instead of showing time, ...

http://skmobi.com/timeismoney/''')

    def test_need_reply(self):
        self.receive_message('/g')
        self.assertReplied(self.bot, 'Google for what?')

        self.receive_message('site:skmobi.com TimeIsMoney')
        self.assertReplied(self.bot, u'''\
skmobi - TimeIsMoney

Time is Money! So, "time" your money with this app. TimeIsMoney uses the \n\
interface you're used to from Clock.app stopwatch, but instead of showing time, ...

http://skmobi.com/timeismoney/''')
