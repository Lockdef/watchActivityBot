from flask import render_template, request, redirect, session
from settings import app
from repositories.user import UserRepository
from twitterApp import TwitterApp

twitterApp = TwitterApp()
user = UserRepository()


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
    return render_template("sucess.html")


@ app.route('/callback', methods=['GET'])
def callback():
    twitterApp.callback()
    return redirect('/')
