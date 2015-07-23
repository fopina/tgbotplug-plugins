# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update
from plugins.google import GooglePlugin


class GooglePluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[GooglePlugin()])

    def test_not_found(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/g site:github.com tgbotplug-plugins',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        # it seems ajax.googleapi.com uses different cache from normal google :/
        # test to be updated one day..
        self.assertReplied(self.bot, 'Sorry, nothing found...')

    def test_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/g site:skmobi.com',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )

        self.assertReplied(self.bot, u'''\
skmobi

skmobi. iPhone Apps · Android Apps · Contact · Layout & Design 100% ripped off. \

Daring Fireball. Copyright © 2012 Filipe Pina.

http://skmobi.com/\
''')

    def test_need_reply(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/g',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'Google for what?')

        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': 'site:skmobi.com',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, u'''\
skmobi

skmobi. iPhone Apps · Android Apps · Contact · Layout & Design 100% ripped off. \

Daring Fireball. Copyright © 2012 Filipe Pina.

http://skmobi.com/\
''')
