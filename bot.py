#!/usr/bin/env python
# coding=utf-8

import tgbot
from plugins.echo import EchoPlugin
from plugins.random_choice import RandomPlugin
from plugins.google import GooglePlugin
from plugins.simsimi import SimsimiPlugin
import argparse

from requests.packages import urllib3
urllib3.disable_warnings()


def main():
    args = build_parser().parse_args()

    tg = tgbot.TGBot(
        args.token,
        plugins=[
            EchoPlugin(),
            GooglePlugin(),
            RandomPlugin(),
        ],
        no_command=SimsimiPlugin(),
        db_url=args.db_url
    )

    if args.list:
        tg.print_commands()
        return

    if args.create_db:
        tg.setup_db()
        print 'DB created'
        return

    if args.webhook is None:
        tg.run(polling_time=args.polling)
    else:
        tg.run_web(args.webhook[0], host='0.0.0.0', port=int(args.webhook[1]))


def build_parser():
    parser = argparse.ArgumentParser(description='Run TestBot')

    parser.add_argument('--polling', '-p', dest='polling', type=float, default=2,
                        help='interval (in seconds) to check for message updates')
    parser.add_argument('--db_url', '-d', dest='db_url', default='sqlite:///testbot.sqlite3',
                        help='URL for database (default is sqlite:///testbot.sqlite3)')
    parser.add_argument('--list', '-l', dest='list', action='store_const', const=True, default=False,
                        help='list commands')
    parser.add_argument('--webhook', '-w', dest='webhook', nargs=2, metavar=('hook_url', 'port'),
                        help='use webhooks (instead of polling) - requires bottle')
    parser.add_argument('--create_db', dest='create_db', action='store_const',
                        const=True, default=False,
                        help='setup database')
    parser.add_argument('--token', '-t', dest='token',
                        help='token provided by @BotFather')

    return parser

if __name__ == '__main__':
    main()
