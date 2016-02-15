from flask import Flask, request

import settings
import json
import telegram
from heating_bot import build_bot

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
bot = None
last_update_id = 0

@app.route("/heatingbot/{0}".format(settings.TG_API_KEY), methods=['GET', 'POST'])
def post():
    body = request.json
    update = telegram.Update.de_json(body)
    message = update.message
    update_id = int(update.update_id)
    if update_id > last_update_id and message and message.text is not None:
        cmd = message.text.lower()
        if cmd.startswith('/on'):
            bot.turnon_cmd(message)
        elif cmd.startswith('/off'):
            bot.turnoff_cmd(message)
        last_update_id = update_id
    return json.dumps(body)

if __name__ == "__main__":
    bot = build_bot(settings.TG_WEB_HOOK, settings.TG_API_KEY)
    app.run()
else:
    bot = build_bot(settings.TG_WEB_HOOK, settings.TG_API_KEY)
