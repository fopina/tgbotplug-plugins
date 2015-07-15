import tgbot


class RandomPlugin(tgbot.TGPluginBase):
    def list_commands(self):
        return [
            ('random', self.random, 'pick a random value from provided list')
        ]

    def random(self, tg, message, text):
        from random import choice
        pars = text.split(' ')
        if pars:
            reply = choice(pars)
        else:
            reply = 'random what?'

        tg.send_message(message.chat.id, reply)
