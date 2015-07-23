from tgbot import plugintest
from twx.botapi import Update
from plugins.echo import EchoPlugin


class EchoPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[EchoPlugin()])

    def test_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/echo test',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'test')

    def test_need_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/echo',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'echo what?')

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': 'test',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'test')
