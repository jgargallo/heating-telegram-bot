from datetime import datetime
from collections import defaultdict
import logging
import telegram
import random

logger = logging.getLogger(__name__)

def build_bot(webhook, apikey):
    bot = telegram.Bot(apikey)
    bot.setWebhook(webhook.format(apikey))
    return HeatingBot(bot)

class HeatingBot(object):

    def __init__(self, bot):
        self.bot = bot

    def turnon_cmd(self, update):
        try:
            self.bot.sendMessage(chat_id=update.chat.id,
                text=u'\U0001F4C6 heating turned on!'.encode('utf-8'))
        except Exception as ex:
            logger.error('new cmd: {0}'.format(ex))

    def turnoff_cmd(self, update):
        try:
            self.bot.sendMessage(chat_id=update.chat.id,
                text=u'\U0001F4C6 heating turned off!'.encode('utf-8'))
        except Exception as ex:
            logger.error('new cmd: {0}'.format(ex))
