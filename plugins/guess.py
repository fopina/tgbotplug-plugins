from __future__ import absolute_import
import tgbot
from twx.botapi import ReplyKeyboardMarkup, ReplyKeyboardHide
import random


class GuessPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(GuessPlugin, self).__init__()
        self.numbers = {}

    def list_commands(self):
        return [
            ('guess_start', self.guess_start, 'start the (number) guess game!'),
            ('guess_stop', self.guess_stop, 'stop the (number) guess game (why? :())')
        ]

    def guess_start(self, bot, message, text):
        number = int(random.random() * 10)
        self.numbers[message.chat.id] = number

        m = bot.tg.send_message(
            message.chat.id,
            "I'm going to think of a number between 0 and 9 and you have to guess it! What's your guess?",
            reply_to_message_id=message.message_id,
            reply_markup=ReplyKeyboardMarkup.create(
                keyboard=[
                    ['0', '1', '2'],
                    ['3', '4', '5'],
                    ['6', '7', '8'],
                    ['9'],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        ).wait()
        self.need_reply(self.guess_try, message, out_message=m, selective=True)

    def guess_try(self, bot, message, text):
        number = self.numbers[message.chat.id]

        done = False

        try:
            guess = int(text)
            if guess == number:
                reply = 'Congratz, you nailed it %s' % message.sender.first_name
                done = True
            elif guess < number:
                reply = "I'm thinking higher..."
            else:
                reply = "I'm thinking lower..."
        except:
            reply = "Invalid guess!"

        if done:
            del(self.numbers[message.chat.id])
            self.clear_chat_replies(message.chat.id)
            bot.tg.send_message(
                message.chat.id,
                reply,
                reply_to_message_id=message.message_id,
                reply_markup=ReplyKeyboardHide.create()
            )
        else:
            m = bot.tg.send_message(
                message.chat.id,
                reply,
                reply_to_message_id=message.message_id,
                reply_markup=ReplyKeyboardMarkup.create(
                    keyboard=[
                        ['0', '1', '2'],
                        ['3', '4', '5'],
                        ['6', '7', '8'],
                        ['9'],
                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                )
            ).wait()
            self.need_reply(self.guess_try, message, out_message=m, selective=True)

    def guess_stop(self, bot, message, text):
        try:
            del(self.numbers[message.chat.id])
        except:
            pass

        self.clear_chat_replies(message.chat.id)

        bot.tg.send_message(
            message.chat.id,
            'Ok :(',
            reply_to_message_id=message.message_id,
            reply_markup=ReplyKeyboardHide.create()
        )
