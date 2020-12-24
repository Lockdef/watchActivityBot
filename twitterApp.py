import json
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session
from flask import jsonify, request
from setting import API_KEY, API_KEY_SECRET, DISCORD_TOKEN
from discordBot import DiscordBot


class TwitterApp():

    def __init__(self):

        self.discordBot = DiscordBot()
        self.discordBot.add_username("Lock")

        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.AUTHENTICATE_URL = 'https://api.twitter.com/oauth/authenticate'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.CALLBACK_URL = 'http://localhost:3334/twitter/callback'
        self.USER_UPDATE_PROFILE_URL = 'https://api.twitter.com/1.1/account/update_profile.json'

    def run_discord_bot(self):
        return self.discordBot.start(DISCORD_TOKEN)

    def get_request_token(self):
        twitter = OAuth1Session(API_KEY, API_KEY_SECRET)
        oauth_callback = request.args.get(self.CALLBACK_URL)
        params = {'oauth_callback': oauth_callback}
        response = twitter.post(self.REQUEST_TOKEN_URL, params=params)
        request_token = dict(parse_qsl(response.content.decode("utf-8")))
        authenticate_endpoint = f'{self.AUTHENTICATE_URL}?oauth_token={request_token["oauth_token"]}'
        request_token.update({'authenticate_endpoint': authenticate_endpoint})
        return jsonify(request_token)

    def callback(self):
        redirect_response = request.url
        twitter = OAuth1Session(API_KEY, API_KEY_SECRET)
        twitter.parse_authorization_response(redirect_response)
        response = twitter.fetch_access_token(self.ACCESS_TOKEN_URL)

        OAUTH_TOKEN = response.get('oauth_token')
        OAUTH_TOKEN_SECRET = response.get('oauth_token_secret')

        twitter = OAuth1Session(API_KEY, API_KEY_SECRET,
                                OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        activity = self.discordBot.activity
        params = {'description': f'Now Playing: {activity}'}

        response = twitter.post(self.USER_UPDATE_PROFILE_URL, params=params)
        results = json.loads(response.text)

        return jsonify(results)
