#!/usr/bin/env python
# coding=utf-8

import tgbot
from requests.packages import urllib3
from plugins.echo import EchoPlugin
from plugins.random import RandomPlugin
from plugins.google import GooglePlugin
from plugins.simsimi import SimsimiPlugin

urllib3.disable_warnings()


def main():
    simsim = SimsimiPlugin()
    tg = tgbot.TGBot(
        'YOUR_BOT_TOKEN',
        plugins=[
            EchoPlugin(),
            GooglePlugin(),
            RandomPlugin(),
        ],
        no_command=simsim.simsimi
    )
    tg.print_commands()
    tg.run()

if __name__ == '__main__':
    main()
