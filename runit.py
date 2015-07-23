#!/usr/bin/env python
# coding=utf-8

import tgbot
from requests.packages import urllib3
from plugins.echo import EchoPlugin
from plugins.random_choice import RandomPlugin
from plugins.google import GooglePlugin
from plugins.simsimi import SimsimiPlugin

urllib3.disable_warnings()


def main():
    tg = tgbot.TGBot(
        'YOUR_BOT_TOKEN',
        plugins=[
            EchoPlugin(),
            GooglePlugin(),
            RandomPlugin(),
        ],
        no_command=SimsimiPlugin()
    )
    tg.print_commands()
    tg.run()

if __name__ == '__main__':
    main()
