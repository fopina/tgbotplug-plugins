#!/usr/bin/env python
# coding=utf-8

import tgbot
from plugins.echo import EchoPlugin
from plugins.random_choice import RandomPlugin
import argparse

from requests.packages import urllib3
urllib3.disable_warnings()


def main():
    args = build_parser().parse_args()

    bot_dbs = ['test1', 'test2']

    bots = [
        tgbot.TGBot(
            args.token1,
            plugins=[
                EchoPlugin(),
            ],
            db_url=args.db_url % bot_dbs[0]
        ),
        tgbot.TGBot(
            args.token2,
            plugins=[
                RandomPlugin(),
            ],
            db_url=args.db_url % bot_dbs[1]
        )
    ]

    if args.list:
        for i, bot in enumerate(bots):
            print 'Bot %d: %s' % (i + 1, bot_dbs[i])
            bot.print_commands()
            print
        return

    if args.create_db:
        for bot in bots:
            bot.setup_db()
            print 'DB created'
        return

    if args.webhook is None:
        from tgbot.tgbot import run_bots
        run_bots(bots, polling_time=args.polling)
    else:
        for bot in bots:
            bot.set_webhook(args.webhook[0] + '/update/' + bot.token)

        from tgbot.webserver import run_server
        run_server(bots, host='0.0.0.0', port=int(args.webhook[1]))


def build_parser():
    parser = argparse.ArgumentParser(description='Run TestBot')

    parser.add_argument('--polling', '-p', dest='polling', type=float, default=0.1,
                        help='interval (in seconds) to check for message updates')
    parser.add_argument('--db_url', '-d', dest='db_url', default='sqlite:///%s.sqlite3',
                        help='URL for database (default is sqlite:///%%s.sqlite3)')
    parser.add_argument('--list', '-l', dest='list', action='store_const', const=True, default=False,
                        help='list commands')
    parser.add_argument('--webhook', '-w', dest='webhook', nargs=2, metavar=('hook_url', 'port'),
                        help='use webhooks (instead of polling) - requires bottle')
    parser.add_argument('--create_db', dest='create_db', action='store_const',
                        const=True, default=False,
                        help='setup database')
    parser.add_argument('--token1', dest='token1',
                        help='token for first bot (provided by @BotFather)')
    parser.add_argument('--token2', dest='token2',
                        help='token for second bot (provided by @BotFather)')

    return parser

if __name__ == '__main__':
    main()
