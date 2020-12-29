import os
from threading import Thread
import asyncio
from flask import Flask, render_template, request, redirect, session
from setting import DISCORD_TOKEN
from twitterApp import TwitterApp
from discordBot import DiscordBot
from db import User

app = Flask(__name__)
app.secret_key = "key"
user = User(app)
twitterApp = TwitterApp(user)
discordBot = DiscordBot(user, twitterApp)


@app.route('/', methods=['GET'])
def index():
    if session.keys() >= {'access_token', 'access_token_secret'}:
        return render_template("set_uid.html")
    redirect_url = twitterApp.get_request_token()
    return render_template("index.html", redirect_url=redirect_url)


@app.route('/', methods=['POST'])
def add_user():
    uid = request.form.get('uid')
    access_token = session['access_token']
    access_token_secret = session['access_token_secret']
    user.add(uid, access_token, access_token_secret)
    return "good"


@ app.route('/callback', methods=['GET'])
def callback():
    twitterApp.callback()
    return redirect('/')


if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    host = '0.0.0.0'
    app_thread = Thread(target=app.run, args=(host, port))
    app_thread.start()
    loop = asyncio.get_event_loop()
    loop.create_task(discordBot.start(DISCORD_TOKEN))
    Thread(target=loop.run_forever())
