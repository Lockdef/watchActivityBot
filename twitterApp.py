import tweepy
import logging
from flask import session, request
from setting import API_KEY, API_KEY_SECRET
import discord


class TwitterApp():
    """
    Twitter関連の処理を行う
    """

    def get_request_token(self) -> str:
        """
        TwitterのログインページへのURLを取得する

        Returns
        -------
        redirect_url : str
            ログインページのURL
        """
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)

        try:
            redirect_url = auth.get_authorization_url()
            session['request_token'] = auth.request_token['oauth_token']
        except tweepy.TweepError as error:
            logging.error(error)

        return redirect_url

    def update_profile(self, activity: discord.activity.Activity) -> dict:
        """
        ユーザーのプロフィールのアクティビティを更新する

        Parameters
        ----------
        activity : discord.activity.Activity
            discordのアクティビティ情報

        Returns
        -------
        result: dict
            update_profileの結果
        """
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
        result = api.update_profile(description=f'Now Playing: {activity}')
        result = result._json
        print(type(result))
        return result
