import tgbot
from twx.botapi import ForceReply


class EchoPlugin(tgbot.TGPluginBase):
    def list_commands(self):
        return [
            ('echo', self.echo, 'right back at ya')
        ]

    def echo(self, bot, message, text):
        if text:
            bot.tg.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
        else:
            m = bot.tg.send_message(
                message.chat.id,
                'echo what?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(
                    selective=True
                )
            ).wait()
            self.need_reply(self.echo, message, out_message=m, selective=True)
