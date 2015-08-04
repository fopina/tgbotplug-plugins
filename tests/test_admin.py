# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update, User
from plugins.admin import AdminPlugin


class AdminPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot(
            '',
            plugins=[AdminPlugin()],
            me=User(99, 'Test', 'Bot', 'test_bot'),
        )
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

    def leave_chat(self, chat, sender=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        self.bot.process_update(
            Update.from_dict({
                'update_id': self.received_id,
                'message': {
                    'message_id': self.received_id,
                    'text': None,
                    'chat': chat,
                    'from': sender,
                    'left_chat_participant': dict(self.bot.tg._bot_user.__dict__),
                }
            })
        )

        self.received_id += 1

    def test_users(self):
        self.receive_message('/users')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '/msg1 - John Doe\n'
        )

        self.receive_message('hey', sender={
            'id': 2,
            'first_name': 'Jane',
            'last_name': 'Doe',
        })

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '''\
/msg1 - John Doe
/msg2 - Jane Doe
''')

    def test_groups(self):
        self.receive_message('/chats')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/chats')
        self.assertReplied(self.bot, 'Zero...')

        self.receive_message(
            'hey',
            chat={
                'id': 1,
                'title': 'chat 1',
            }
        )

        self.receive_message('/chats')
        self.assertReplied(self.bot, '/msg1 - chat 1\n')

        self.receive_message(
            'hey',
            chat={
                'id': 2,
                'title': 'chat 2',
            }
        )

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            '''\
/msg1 - chat 1
/msg2 - chat 2
''')

        self.leave_chat(
            {
                'id': 1,
                'title': 'chat 1',
            }
        )

        self.receive_message('/chats')
        self.assertReplied(self.bot, '/msg2 - chat 2\n')

    def test_more_users(self):
        self.receive_message('/more')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

        self.receive_message('/users')
        self.assertReplied(self.bot, '/msg1 - John Doe\n')

        for i in xrange(2, 11):
            self.receive_message('hey', sender={
                'id': i,
                'first_name': 'Jane',
                'last_name': str(i),
            })
        self.receive_message('hey', sender={
            'id': -1,
            'first_name': 'Jane',
            'last_name': '-1',
        })

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '''\
/msgN1 - Jane -1
/msg1 - John Doe
/msg2 - Jane 2
/msg3 - Jane 3
/msg4 - Jane 4
/msg5 - Jane 5
/msg6 - Jane 6
/msg7 - Jane 7
/msg8 - Jane 8
/msg9 - Jane 9
There are more, type /more to list 10 more results''')

        self.receive_message('/more')
        self.assertReplied(self.bot, '/msg10 - Jane 10\n')
        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

    def test_more_chats(self):
        self.receive_message('/more')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

        self.receive_message('/chats')
        self.assertReplied(self.bot, 'Zero...')

        for i in xrange(-1, 20):
            self.receive_message('hey', chat={
                'id': i,
                'title': 'chat %d' % i,
            })

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            '''\
/msgN1 - chat -1
/msg0 - chat 0
/msg1 - chat 1
/msg2 - chat 2
/msg3 - chat 3
/msg4 - chat 4
/msg5 - chat 5
/msg6 - chat 6
/msg7 - chat 7
/msg8 - chat 8
There are more, type /more to list 10 more results''')

        self.receive_message('/more')
        self.receive_message('/more')
        self.assertReplied(self.bot, '/msg19 - chat 19\n')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

    def test_change_password(self):
        self.receive_message('/newpass')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/newpass otherpassword')
        self.assertReplied(
            self.bot, '''\
Password updated to:
otherpassword''')

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, 'You are already admin')

        sender = {
            'id': 2,
            'first_name': 'Jane',
            'last_name': 'Doe',
        }
        self.clear_replies(self.bot)
        self.receive_message('/auth changeme', sender=sender)
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth otherpassword', sender=sender)
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

    def test_message(self):
        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, u'Welcome \U0001F60F')

        self.receive_message('/msg1 hello')
        self.assertReplied(self.bot, "'hello' sent to 1")

        self.receive_message('/msg 1 bye')
        self.assertReplied(self.bot, "'bye' sent to 1")

        self.receive_message('/msg1')
        self.assertReplied(self.bot, "And say what?")

        self.receive_message('hey again')
        self.assertReplied(self.bot, "'hey again' sent to 1")
