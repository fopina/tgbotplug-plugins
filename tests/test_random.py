from tgbot import plugintest
from twx.botapi import Update
from plugins.random_choice import RandomPlugin


class RandomPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[RandomPlugin()])

    def test_need_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/random',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'What are the options? (space separated)')

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': 'foo bar',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        try:
            self.assertReplied(self.bot, 'foo')
        except AssertionError:
            self.assertReplied(self.bot, 'bar')

    def test_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/random foo bar',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        self.assertIn(
            self.last_reply(self.bot),
            [
                'foo',
                'bar',
            ]
        )