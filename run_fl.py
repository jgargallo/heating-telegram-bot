from flask import Flask, request

import settings
import json
import telegram
from heating_bot import build_bot

app = Flask(__name__)
bot = None

@app.route("/heatingbot/{0}".format(settings.TG_API_KEY), methods=['GET', 'POST'])
def post():
    body = request.json
    message = telegram.Update.de_json(body).message
    if message and message.text is not None:
        cmd = message.text.lower()
        if cmd.startswith('/on'):
            bot.turnon_cmd(message)
        elif cmd.startswith('/off'):
            bot.turnoff_cmd(message)
    return json.dumps(body)

if __name__ == "__main__":
    bot = build_bot(settings.TG_WEB_HOOK, settings.TG_API_KEY)
    app.run()
else:
    bot = build_bot(settings.TG_WEB_HOOK, settings.TG_API_KEY)
