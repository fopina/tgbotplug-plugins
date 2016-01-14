# tgbotplug-plugins
Plugin Examples for [tgbotplug](https://github.com/fopina/tgbotplug)  
[![Build Status](https://travis-ci.org/fopina/tgbotplug-plugins.svg)](https://travis-ci.org/fopina/tgbotplug-plugins) [![Coverage Status](https://coveralls.io/repos/fopina/tgbotplug-plugins/badge.svg?branch=master&service=github)](https://coveralls.io/github/fopina/tgbotplug-plugins?branch=master)

## Usage

    git clone https://github.com/fopina/tgbotplug-plugins/
    pip install -r requirements.txt

And then either run _bot.py_ (specifying your bot token) or you can run the library directly from command line passing these plugins (and your own) as parameters:

    python -m tgbot -t YOUR_BOT_TOKEN -n plugins.simsimi.SimsimiPlugin \
    plugins.echo.EchoPlugin plugins.random.RandomPlugin plugins.google.GooglePlugin \
    plugins.guess.GuessPlugin plugins.admin.AdminPlugin

_echo_ and _random_ are the simplest plugins, use _TelegramBot.send_message_ and _TGBot.need_reply_  
_google_ is an example on how to use _TelegramBot.send_photo_  
_guess_ shows off plugin data persistence using _TGPluginBase.save_data_ and _TGPluginBase.read_data_  
Check _simsimi_ for a non-command plugin example.

You can also check _multibot.py_ for an example on how to run multiple bots in the same process.  
You can run try it with:

    ./multibot.py --token1 YOUR_BOT1_TOKEN --token2 YOUR_BOT2_TOKEN

`BOT1` will answer to `/echo` command and `BOT2` to `/random`.
