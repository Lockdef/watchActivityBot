import os
from threading import Thread
import asyncio
from flask import Flask
from twitter import TwitterApp

app = Flask(__name__)
app.secret_key = "key"
twitterApp = TwitterApp()


@app.route('/twitter/request_token', methods=['GET'])
def get_request_token():
    return twitterApp.get_request_token()


@app.route('/twitter/callback')
def callback():
    return twitterApp.callback()


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    host = '0.0.0.0'
    app_thread = Thread(target=app.run, args=(host, port))
    app_thread.start()
    loop = asyncio.get_event_loop()
    loop.create_task(twitterApp.run_discord_bot())
    Thread(target=loop.run_forever())
