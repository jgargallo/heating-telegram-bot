DEBUG = True

#Telegram bot api_key
TG_API_KEY='xxx'
TG_WEB_HOOK = 'https://golean.do/heatingbot/{0}'

# local settings must be placed in a file named 'local_settings.py' next to settings.py
try:
   from local_settings import *
except ImportError:
   pass
