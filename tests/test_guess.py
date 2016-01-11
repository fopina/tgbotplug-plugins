from tgbot import plugintest
from tgbot.botapi import Update
from plugins.guess import GuessPlugin


class GuessPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.plugin = GuessPlugin()
        self.bot = self.fake_bot('', plugins=[self.plugin])
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

    def test_play(self):
        self.receive_message('/guess_start')
        self.assertReplied(self.bot, "I'm going to think of a number between 0 and 9 and you have to guess it! What's your guess?")

        number = self.plugin.read_data(1)
        self.assertIsNotNone(number)
        self.assertGreaterEqual(number, 0)
        self.assertLessEqual(number, 9)

        # force number for testing
        self.plugin.save_data(1, obj=5)

        self.receive_message('1')
        self.assertReplied(self.bot, "I'm thinking higher...")

        self.receive_message('6')
        self.assertReplied(self.bot, "I'm thinking lower...")

        self.receive_message('gief error')
        self.assertReplied(self.bot, 'Invalid guess!')

        self.receive_message('5')
        self.assertReplied(self.bot, 'Congratz, you nailed it John')
