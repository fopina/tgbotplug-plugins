from tgbot.pluginbase import TGPluginBase, TGCommandBase
from tgbot.botapi import ForceReply


class EchoPlugin(TGPluginBase):
    def list_commands(self):
        return (
            TGCommandBase('echo', self.echo, 'right back at ya'),
        )

    def echo(self, message, text):
        if text:
            self.bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
        else:
            m = self.bot.send_message(
                message.chat.id,
                'echo what?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(
                    selective=True
                )
            ).wait()
            self.need_reply(self.echo, message, out_message=m, selective=True)
