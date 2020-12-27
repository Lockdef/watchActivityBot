import os
from threading import Thread
import asyncio
from flask import Flask, render_template
from setting import DISCORD_TOKEN
from twitterApp import TwitterApp
from discordBot import DiscordBot

app = Flask(__name__)
app.secret_key = "key"
twitterApp = TwitterApp()
discordBot = DiscordBot()
discordBot.add_username('Lock')


@app.route('/', methods=['GET'])
def index():
    redirect_url = twitterApp.get_request_token()
    return render_template("index.html", redirect_url=redirect_url)


@ app.route('/callback', methods=['GET'])
def callback():
    return "Succeful." if twitterApp.update_profile(discordBot.get_activity(username="Lock")) else "Failed."


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    host = '0.0.0.0'
    app_thread = Thread(target=app.run, args=(host, port))
    app_thread.start()
    loop = asyncio.get_event_loop()
    loop.create_task(discordBot.start(DISCORD_TOKEN))
    Thread(target=loop.run_forever())
