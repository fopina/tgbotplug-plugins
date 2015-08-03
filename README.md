# tgbotplug-plugins
Plugin Examples for [tgbotplug](https://github.com/fopina/tgbotplug)  
[![Build Status](https://travis-ci.org/fopina/tgbotplug-plugins.svg)](https://travis-ci.org/fopina/tgbotplug-plugins)

## Usage

    git clone https://github.com/fopina/tgbotplug-plugins/
    pip install -r requirements.txt

And then either run _runit.py_ (after adding your bot token) or you can run the library directly from command line passing these plugins (and your own) as parameters:

    python -m tgbot -t YOUR_BOT_TOKEN -n plugins.simsimi.SimsimiPlugin \
    plugins.echo.EchoPlugin plugins.random.RandomPlugin plugins.google.GooglePlugin \
    plugins.guess.GuessPlugin plugins.admin.AdminPlugin
    
_echo_ and _random_ are the simplest plugins, use _TelegramBot.send_message_ and _TGBot.need_reply_  
_google_ is an example on how to use _TelegramBot.send_photo_  
_guess_ shows off plugin data persistence using _TGPluginBase.save_data_ and _TGPluginBase.read_data_  
Check _simsimi_ for a non-command plugin example.
