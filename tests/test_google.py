# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update
from plugins.google import GooglePlugin


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
        self.receive_message('/g site:skmobi.com')
        self.assertReplied(self.bot, u'''\
skmobi

skmobi. iPhone Apps · Android Apps · Contact · Layout & Design 100% ripped off. \

Daring Fireball. Copyright © 2012 Filipe Pina.

http://skmobi.com/\
''')

    def test_need_reply(self):
        self.receive_message('/g')
        self.assertReplied(self.bot, 'Google for what?')

        self.receive_message('site:skmobi.com')
        self.assertReplied(self.bot, u'''\
skmobi

skmobi. iPhone Apps · Android Apps · Contact · Layout & Design 100% ripped off. \

Daring Fireball. Copyright © 2012 Filipe Pina.

http://skmobi.com/\
''')
