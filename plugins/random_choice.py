import tgbot
from random import choice
from twx.botapi import ForceReply


class RandomPlugin(tgbot.TGPluginBase):
    def list_commands(self):
        return [
            ('random', self.random, 'pick a random value from provided list')
        ]

    def random(self, bot, message, text):
        if not text:
            m = bot.tg.send_message(
                message.chat.id,
                'What are the options? (space separated)',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(selective=True)
            ).wait()
            self.need_reply(self.random, message, out_message=m, selective=True)
        else:
            pars = text.split()  # split on any whitespace
            reply = choice(pars)
            bot.tg.send_message(message.chat.id, reply, reply_to_message_id=message.message_id)