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
        self.assertReplied(self.bot, 'Welcome :-)')

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '1 - John Doe\n'
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
1 - John Doe
2 - Jane Doe
''')

    def test_groups(self):
        self.receive_message('/chats')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, 'Welcome :-)')

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            'No chats...'
        )

        self.receive_message(
            'hey',
            chat={
                'id': 1,
                'title': 'chat 1',
            }
        )

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            '''\
1 - chat 1
''')

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
1 - chat 1
2 - chat 2
''')

        self.leave_chat(
            {
                'id': 1,
                'title': 'chat 1',
            }
        )

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            '''\
2 - chat 2
''')

    def test_more_users(self):
        self.receive_message('/more')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, 'Welcome :-)')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '1 - John Doe\n'
        )

        for i in xrange(2, 15):
            self.receive_message('hey', sender={
                'id': i,
                'first_name': 'Jane',
                'last_name': str(i),
            })

        self.receive_message('/users')
        self.assertReplied(
            self.bot,
            '''\
1 - John Doe
2 - Jane 2
3 - Jane 3
4 - Jane 4
5 - Jane 5
6 - Jane 6
7 - Jane 7
8 - Jane 8
9 - Jane 9
10 - Jane 10
There are more users, type /more to list 10 more results''')

        self.receive_message('/more')
        self.assertReplied(
            self.bot,
            '''\
11 - Jane 11
12 - Jane 12
13 - Jane 13
14 - Jane 14
''')
        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

    def test_more_chats(self):
        self.receive_message('/more')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, 'Welcome :-)')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

        self.receive_message('/chats')
        self.assertReplied(self.bot, 'No chats...')

        for i in xrange(1, 22):
            self.receive_message('hey', chat={
                'id': i,
                'title': 'chat %d' % i,
            })

        self.receive_message('/chats')
        self.assertReplied(
            self.bot,
            '''\
1 - chat 1
2 - chat 2
3 - chat 3
4 - chat 4
5 - chat 5
6 - chat 6
7 - chat 7
8 - chat 8
9 - chat 9
10 - chat 10
There are more groups, type /more to list 10 more results''')

        self.receive_message('/more')
        self.receive_message('/more')
        self.assertReplied(
            self.bot,
            '''\
21 - chat 21
''')

        self.receive_message('/more')
        self.assertReplied(self.bot, 'No pending query...')

    def test_change_password(self):
        self.receive_message('/newpass')
        self.assertRaises(AssertionError, self.last_reply, self.bot)

        self.receive_message('/auth changeme')
        self.assertReplied(self.bot, 'Welcome :-)')

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
        self.assertReplied(self.bot, 'Welcome :-)')
