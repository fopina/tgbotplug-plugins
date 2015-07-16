import tgbot


class EchoPlugin(tgbot.TGPluginBase):
    def list_commands(self):
        return [
            ('echo', self.echo, 'right back at ya')
        ]

    def echo(self, bot, message, text):
        reply = text
        if not reply:
            reply = 'echo'
        bot.tg.send_message(message.chat.id, reply, reply_to_message_id=message.message_id)
