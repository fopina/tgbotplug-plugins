# coding=utf-8
from tgbot import plugintest
from tgbot.botapi import Update
from plugins.simsimi import SimsimiPlugin


class SimsimiPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[], no_command=SimsimiPlugin())
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

    def test_reply(self):
        self.receive_message('hello')

        # any reply will do...
        self.last_reply(self.bot)

    def test_no_reply(self):
        self.receive_message('')

        # any reply will do...
        self.assertRaisesRegexp(AssertionError, 'No replies', self.last_reply, self.bot)
