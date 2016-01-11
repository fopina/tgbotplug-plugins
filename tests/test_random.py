from tgbot import plugintest
from tgbot.botapi import Update
from plugins.random_choice import RandomPlugin


class RandomPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[RandomPlugin()])
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

    def test_need_reply(self):
        self.receive_message('/random')
        self.assertReplied(self.bot, 'What are the options? (space separated)')

        self.receive_message('foo bar')

        self.assertIn(
            self.last_reply(self.bot),
            [
                'foo',
                'bar',
            ]
        )

    def test_reply(self):
        self.receive_message('/random foo bar')

        self.assertIn(
            self.last_reply(self.bot),
            [
                'foo',
                'bar',
            ]
        )
