#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import time, threading
import sys
from telegram import Updater
import logging
import settings
#import img
import img_plotly as img
from datetime import datetime

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

value = None
try:
    sys.path.insert(0, '/usr/lib/python2.7/bridge/')
    from bridgeclient import BridgeClient as bridgeclient
    #from tcp import TCPJSONClient
    #json = TCPJSONClient('127.0.0.1', 5700)
    value = bridgeclient()
except:
    logger.warn('No Bridge support')

last_update_id = 0

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text='me no compredo')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def msg_allowed(update):
    global last_update_id
    if update.message.from_user.id in settings.TG_ALLOWED_USERS and update.update_id > last_update_id:
        last_update_id = update.update_id
        return True
    return False

def send_plot(bot, update, date, day):
    img_file = img.plot(date, day)
    logger.info(img_file)
    #bot.sendPhoto(chat_id=update.message.chat_id, photo=open(img_file, 'rb'))
    bot.sendPhoto(chat_id=update.message.chat_id, photo=img_file)

def cmd_on(bot, update, args):
    if msg_allowed(update):
    	#json.send({'command':'put', 'key':'D13', 'value':'1'})
        if value:
    	    value.put('D13','1')
        bot.sendMessage(update.message.chat_id, text='heating turned on!')

def cmd_off(bot, update, args):
    if msg_allowed(update):
        bot.sendMessage(update.message.chat_id, text='heating turned off!')
        date = datetime.now()
        send_plot(bot, update, date, not 'month' in update.message.text.lower())

def cmd_check(bot, update, args):
    if msg_allowed(update):
        v = 'Arduino disconected'
        if value:
    	    v = value.get('CHECK')
        bot.sendMessage(update.message.chat_id, text=v)
        date = datetime.now()
        send_plot(bot, update, date, not 'month' in update.message.text.lower())

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(settings.TG_API_KEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("on", cmd_on)
    dp.addTelegramCommandHandler("off", cmd_off)
    dp.addTelegramCommandHandler("check", cmd_check)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
