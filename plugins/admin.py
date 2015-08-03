import tgbot
from twx.botapi import Error


class AdminPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(AdminPlugin, self).__init__()

    def list_commands(self):
        return [
            ('users', self.list_users, 'List known users'),
            ('chats', self.list_chats, 'List active chats'),
            ('more', self.more, 'List 10 more hits'),
            ('msg', self.msg, 'Send message to user/chat'),
        ]

    def list_users(self, bot, message, text):
        msg = ''
        cnt = 0
        for u in tgbot.models.User.select().paginate(1, 10):
            cnt += 1
            msg += '%s - %s %s\n' % (
                u.id,
                u.first_name,
                u.last_name,
            )

        if cnt == 10:
            msg += 'There are more users, type /more to list 10 more results'
            self.save_data(message.chat.id, obj={'more': 'user', 'page': 1})
        elif cnt == 0:
            msg = 'No users...'

        bot.tg.send_message(message.chat.id, msg)

    def list_chats(self, bot, message, text):
        msg = ''
        cnt = 0
        for u in tgbot.models.GroupChat.select().paginate(1, 10):
            cnt += 1
            msg += '%s - %s\n' % (
                u.id,
                u.title,
            )

        if cnt == 10:
            msg += 'There are more groups, type /more to list 10 more results'
            self.save_data(message.chat.id, obj={'more': 'chat', 'page': 1})
        elif cnt == 0:
            msg = 'No chats...'

        bot.tg.send_message(message.chat.id, msg)

    def msg(self, bot, message, text):
        p = text.find(' ')
        cid = text[:p]
        msg = text[p + 1:]
        m = bot.tg.send_message(cid, msg).wait()
        if isinstance(m, Error):
            bot.tg.send_message(message.chat.id, "Failed to send message:\n%s (%d)" % (m.description, m.error_code))
        else:
            bot.tg.send_message(message.chat.id, "'%s' sent to %s" % (msg, cid))

    def more(self, bot, message, text):
        more = self.read_data(message.chat.id)

        if more is None:
            bot.tg.send_message(message.chat.id, 'No pending query...')
            return

        msg = ''
        cnt = 0

        more['page'] += 1
        if more['more'] == 'chat':
            for u in tgbot.models.GroupChat.select().paginate(more['page'], 10):
                cnt += 1
                msg += '%s - %s\n' % (
                    u.id,
                    u.title,
                )
        elif more['more'] == 'user':
            for u in tgbot.models.User.select().paginate(more['page'], 10):
                cnt += 1
                msg += '%s - %s %s\n' % (
                    u.id,
                    u.first_name,
                    u.last_name,
                )

        if cnt == 10:
            msg += 'Type /more to list 10 more results'
            self.save_data(message.chat.id, obj=more)
        else:
            if cnt == 0:
                msg = 'Nothing left...'
            self.save_data(message.chat.id)

        bot.tg.send_message(message.chat.id, msg)