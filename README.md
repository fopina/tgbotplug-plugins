# tgbotplug-plugins
Plugin Examples for [tgbotplug](https://github.com/fopina/tgbotplug)  
[![Build Status](https://travis-ci.org/fopina/tgbotplug-plugins.svg)](https://travis-ci.org/fopina/tgbotplug-plugins)

## Usage

    git clone https://github.com/fopina/tgbotplug-plugins/
    pip install -r requirements.txt

And then either run _runit.py_ (after adding your bot token) or you can run the library directly from command line passing these plugins (and your own) as parameters:

    python -m tgbot -t YOUR_BOT_TOKEN -n plugins.simsimi.SimsimiPlugin plugins.echo.EchoPlugin plugins.random.RandomPlugin plugins.google.GooglePlugin
    
Check _echo, google_ and _random_ for simple reply command examples (also using _need_reply_).  
Check _guess_ for an example a little bit more elaborated.  
Check _simsimi_ for a non-command plugin example.
