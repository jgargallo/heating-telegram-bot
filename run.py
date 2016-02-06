# -*- coding: utf-8 -*-

import settings

from heating_bot import build_bot
from requests.packages import urllib3

if __name__ == "__main__":
    urllib3.disable_warnings()

    bot = build_bot(settings.TG_WEB_HOOK, settings.TG_API_KEY)
    bot.start()


