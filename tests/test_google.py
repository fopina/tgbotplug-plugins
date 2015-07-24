# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update
from plugins.google import GooglePlugin
import re


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
        # it seems ajax.googleapi.com uses different cache from normal google :/
        # test to be updated one day..
        self.assertReplied(self.bot, 'Sorry, nothing found...')

    def test_reply(self):
        self.receive_message('/g site:github.com tgbotplug')
        # remove 'X days ago' from reply for longer-lasting match!
        reply = re.sub('\d+ \w+ ago', '', self.last_reply(self.bot))

        self.assertEqual(reply, u'''\
fopina/tgbotplug · GitHub

 ... Telegram plugin-based bot. Contribute to tgbotplug development by creating an \n\
account on GitHub.

https://github.com/fopina/tgbotplug/tree/master\
''')

    def test_need_reply(self):
        self.receive_message('/g')
        self.assertReplied(self.bot, 'Google for what?')

        self.receive_message('site:github.com tgbotplug')
        # remove 'X days ago' from reply for longer-lasting match!
        reply = re.sub('\d+ \w+ ago', '', self.last_reply(self.bot))

        self.assertEqual(reply, u'''\
fopina/tgbotplug · GitHub

 ... Telegram plugin-based bot. Contribute to tgbotplug development by creating an \n\
account on GitHub.

https://github.com/fopina/tgbotplug/tree/master\
''')
