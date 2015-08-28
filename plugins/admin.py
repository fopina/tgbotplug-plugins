import tgbot
from twx.botapi import Error, ForceReply
import hashlib


class AdminPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(AdminPlugin, self).__init__()
        self.__default_pwd = hashlib.sha256('changeme').hexdigest()

    def list_commands(self):
        return (
            tgbot.TGCommandBase('users', self.list_users, 'List known users', printable=False),
            tgbot.TGCommandBase('chats', self.list_chats, 'List active chats', printable=False),
            tgbot.TGCommandBase('more', self.more, 'List 10 more hits', printable=False),
            tgbot.TGCommandBase('msg', self.msg, 'Send message to user/chat', prefix=True, printable=False),
            tgbot.TGCommandBase('newpass', self.newpass, 'Change admin password', printable=False),
            tgbot.TGCommandBase('auth', self.auth, 'Authenticate as admin', printable=False),
        )

    def __is_admin(self, message):
        obj = self.read_data(message.chat.id, key2='ADMIN')
        return obj is True

    def auth(self, bot, message, text):
        if self.__is_admin(message):
            bot.send_message(message.chat.id, 'You are already admin')
        else:
            phash = self.read_data('ADMINPWD')
            if phash is None:
                phash = self.__default_pwd

            if hashlib.sha256(text).hexdigest() == phash:
                self.save_data(message.chat.id, key2='ADMIN', obj=True)
                bot.send_message(message.chat.id, u'Welcome \U0001F60F')

    def newpass(self, bot, message, text):
        if self.__is_admin(message) and text:
            self.save_data('ADMINPWD', obj=hashlib.sha256(text).hexdigest())
            bot.send_message(message.chat.id, 'Password updated to:\n' + text)

    def list(self, bot, message, model_cls, page=1):
        msg = ''
        cnt = 0
        for u in model_cls.select().paginate(page, 10):
            cnt += 1

            nid = u.id
            if nid < 0:
                nid = 'N' + str(nid * -1)  # much faster than abs..

            if model_cls == tgbot.models.User:
                msg += '/msg%s - %s %s\n' % (
                    nid,
                    u.first_name,
                    u.last_name,
                )
            else:
                msg += '/msg%s - %s\n' % (
                    nid,
                    u.title,
                )

        if cnt == 10:
            msg += 'There are more, type /more to list 10 more results'
            self.save_data(message.chat.id, obj={'more': model_cls.__name__, 'page': page})
        elif cnt == 0:
            msg = 'Zero...'
            self.save_data(message.chat.id)
        else:
            self.save_data(message.chat.id)

        bot.send_message(message.chat.id, msg)

    def list_users(self, bot, message, text):
        if not self.__is_admin(message):
            return
        self.list(bot, message, tgbot.models.User)

    def list_chats(self, bot, message, text, page=1):
        if not self.__is_admin(message):
            return
        self.list(bot, message, tgbot.models.GroupChat)

    def msg(self, bot, message, text):
        if not self.__is_admin(message):
            return

        if text == '':
            bot.send_message(message.chat.id, 'Use /users or /chats to list available ids')
            return

        p = text.find(' ')
        if p < 0:
            self.save_data(message.chat.id, key2='msg', obj=text)
            m = bot.send_message(
                message.chat.id,
                'And say what?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(selective=True)
            ).wait()
            self.need_reply(self.forward_message, message, out_message=m, selective=True)
            return

        cid = text[:p]
        msg = text[p + 1:]

        self.forward_message(bot, message, msg, dst=cid)

    def forward_message(self, bot, message, msg, dst=None):
        if dst is None:
            dst = self.read_data(message.chat.id, key2='msg')
            self.save_data(message.chat.id, key2='msg')

        if dst is None:
            bot.send_message(message.chat.id, 'Something went wrong...')
            return

        if dst[0] == 'N':
            dst = '-' + dst[1:]

        m = bot.send_message(dst, msg).wait()
        if isinstance(m, Error):
            bot.send_message(message.chat.id, "Failed to send message:\n%s (%d)" % (m.description, m.error_code))
        else:
            bot.send_message(message.chat.id, "'%s' sent to %s" % (msg, dst))

    def more(self, bot, message, text):
        if not self.__is_admin(message):
            return

        more = self.read_data(message.chat.id)

        if more is None:
            bot.send_message(message.chat.id, 'No pending query...')
            return

        more['page'] += 1
        if more['more'] == 'GroupChat':
            self.list(bot, message, tgbot.models.GroupChat, page=more['page'])
        elif more['more'] == 'User':
            self.list(bot, message, tgbot.models.User, page=more['page'])
