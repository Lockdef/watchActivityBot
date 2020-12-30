from settings import db
import sys
sys.path.append('../')


class UserModel(db.Model):
    """
            ユーザーのモデルクラス

            Parameters
            ----------
            uid : int
                discordユーザーのid
            access_token : str
                twitterのoauthのapikey
            access_token_secret : str
                twitterのoauthのapikeysecret

            Attributes
            ----------
            uid : int
                discordユーザーのid
            access_token : str
                twitterのoauthのapikey
            access_token_secret : str
                twitterのoauthのapikeysecret
            """
    uid = db.Column(db.Integer(), primary_key=True)
    access_token = db.Column(db.String(27), unique=True)
    access_token_secret = db.Column(db.String(32), unique=True)

    def __init__(self, uid: int, access_token: str, access_token_secret: str):
        self.uid = uid
        self.access_token = access_token
        self.access_token_secret = access_token_secret
