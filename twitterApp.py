import tweepy
import logging
from flask import session, request
from settings import API_KEY, API_KEY_SECRET
from repositories.user import UserRepository

user = UserRepository()


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

    def callback(self):
        """
        callbackURLからtokenを取得する
        """
        token = session.pop('request_token', None)
        verifier = request.args.get('oauth_verifier')
        if token is None or verifier is None:
            return False
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.request_token = {'oauth_token': token,
                              'oauth_token_secret': verifier}
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Error! Failed to get access token.')

        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret

    def update_profile(self, uid: int, activity: str) -> dict:
        """
        ユーザーのプロフィールのアクティビティを更新する

        Parameters
        ----------
        uid : int
            対象ユーザーのid
        activity : discord.activity.Activity
            discordのアクティビティ情報

        Returns
        -------
        result: dict
            update_profileの結果
        """
        user_ = user.read_by_uid(uid)
        key = user_.access_token
        secret = user_.access_token_secret
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        # description: str = api.get_user().description
        # description.replace("%a", activity)
        description = f'{activity}をプレイ中'
        result = api.update_profile(description=description)
        result = result._json
        return "OK" if result else "NG"
