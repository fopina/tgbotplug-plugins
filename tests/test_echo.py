from tgbot import plugintest
from twx.botapi import Update
from plugins.echo import EchoPlugin


class EchoPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[EchoPlugin()])
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
        self.receive_message('/echo test')
        self.assertReplied(self.bot, 'test')

    def test_need_reply(self):
        self.receive_message('/echo')
        self.assertReplied(self.bot, 'echo what?')

        self.receive_message('test')
        self.assertReplied(self.bot, 'test')
