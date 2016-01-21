# coding=utf-8
from tgbot import plugintest
from tgbot.botapi import Update
from plugins.simsimi import SimsimiPlugin
import os

from requests.packages import urllib3
urllib3.disable_warnings()


class SimsimiPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self._key = os.environ.get('SIMSIMI_KEY', '')
        self.bot = self.fake_bot('', plugins=[], no_command=SimsimiPlugin(self._key))
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
        # if no key configured, use mock
        if not self._key:
            import mock

            def fget(*args, **kwargs):
                r = type('Test', (object,), {})()
                r.json = lambda: {'result': 100, 'response': 'hello'}
                return r

            with mock.patch('requests.get', fget):
                self.receive_message('hello')
        else:
            self.receive_message('hello')

        # any reply will do except the error reply
        self.assertNotEqual(self.last_reply(self.bot), 'Sorry, sleeping at the moment...')

    def test_no_reply(self):
        self.receive_message('')

        # any reply will do...
        self.assertRaisesRegexp(AssertionError, 'No replies', self.last_reply, self.bot)
