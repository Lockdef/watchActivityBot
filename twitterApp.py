import tweepy
import logging
from flask import session, redirect, request
from setting import API_KEY, API_KEY_SECRET, DISCORD_TOKEN
from discordBot import DiscordBot


class TwitterApp():

    def __init__(self):
        self.discordBot = DiscordBot()
        self.discordBot.add_username("Lock")

    def run_discord_bot(self):
        return self.discordBot.start(DISCORD_TOKEN)

    def get_request_token(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)

        try:
            redirect_url = auth.get_authorization_url()
            session['request_token'] = auth.request_token['oauth_token']
        except tweepy.TweepError as error:
            logging.error(error)
        return redirect(redirect_url)

    def callback(self):
        if 'request_token' not in session:
            return False
        token = session.pop('request_token', None)
        verifier = request.args.get('oauth_verifier')
        if token is None or verifier is None:
            return False
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.request_token = {'oauth_token': token,
                              'oauth_token_secret': verifier}
        auth.get_access_token(verifier)
        api = tweepy.API(auth)
        activity = self.discordBot.activity
        result = api.update_profile(description=f'Now Playing: {activity}')
        return result._json
