import json
import os
from typing import Final
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session
from flask import Flask, jsonify, request
from setting import API_KEY, API_KEY_SECRET

app = Flask(__name__)

REQUEST_TOKEN_URL: Final[str] = 'https://api.twitter.com/oauth/request_token'
AUTHENTICATE_URL: Final[str] = 'https://api.twitter.com/oauth/authenticate'
ACCESS_TOKEN_URL: Final[str] = 'https://api.twitter.com/oauth/access_token'
CALLBACK_URL: Final[str] = 'http://localhost:3334/twitter/callback'
USER_UPDATE_PROFILE_URL: Final[str] = 'https://api.twitter.com/1.1/account/update_profile.json'


@app.route('/twitter/request_token', methods=['GET'])
def get_twitter_request_token():

    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = request.args.get(USER_UPDATE_PROFILE_URL)

    twitter = OAuth1Session(API_KEY, API_KEY_SECRET)

    response = twitter.post(
        REQUEST_TOKEN_URL,
        params={'oauth_callback': oauth_callback}
    )

    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから認証画面のURLを生成
    authenticate_endpoint = f'%s?oauth_token=%s' \
        % (AUTHENTICATE_URL, request_token['oauth_token'])

    request_token.update({'authenticate_endpoint': authenticate_endpoint})

    return jsonify(request_token)


# 成功！！
@app.route('/twitter/callback')
def callback():
    redirect_response = request.url
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET)
    twitter.parse_authorization_response(redirect_response)
    response = twitter.fetch_access_token(ACCESS_TOKEN_URL)

    AT = response.get('oauth_token')
    AS = response.get('oauth_token_secret')

    twitter = OAuth1Session(
        API_KEY,
        API_KEY_SECRET,
        AT,
        AS
    )
    params = {
        'description': '負けた'
    }

    response = twitter.post(USER_UPDATE_PROFILE_URL, params=params)
    results = json.loads(response.text)

    return jsonify(results)

if __name__ == "__main__":
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )
