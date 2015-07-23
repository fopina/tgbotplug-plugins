# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update
from plugins.simsimi import SimsimiPlugin


class EchoPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[], no_command=SimsimiPlugin())

    def test_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': 'hello',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        # any reply will do...
        self.last_reply(self.bot)
