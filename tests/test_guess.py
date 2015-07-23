from tgbot import plugintest
from twx.botapi import Update
from plugins.guess import GuessPlugin


class GuessPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.plugin = GuessPlugin()
        self.bot = self.fake_bot('', plugins=[self.plugin])

    def test_play(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/guess_start',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, "I'm going to think of a number between 0 and 9 and you have to guess it! What's your guess?")
        self.assertIn(1, self.plugin.numbers)
        self.assertGreaterEqual(self.plugin.numbers[1], 0)
        self.assertLessEqual(self.plugin.numbers[1], 9)

        # force number for testing
        self.plugin.numbers[1] = 5

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '1',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        self.assertReplied(self.bot, "I'm thinking higher...")

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '6',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        self.assertReplied(self.bot, "I'm thinking lower...")

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': 'error?',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        self.assertReplied(self.bot, 'Invalid guess!')

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '5',
                    'chat': {
                        'id': 1,
                    },
                    'from': {
                        'first_name': 'John',
                        'last_name': 'Doe',
                    }
                }
            })
        )

        self.assertReplied(self.bot, 'Congratz, you nailed it John')