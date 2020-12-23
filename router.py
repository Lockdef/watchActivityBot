import os
from flask import Flask
from twitterApp import TwitterApp

app = Flask(__name__)
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
    app.run(
        host=host,
        port=port,
    )
