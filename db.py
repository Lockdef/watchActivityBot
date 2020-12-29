import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class User():
    """
    ユーザーデータベースへの操作全般を扱うクラス

    Parameters
    ----------
    app : Flask
        Flaskのインスタンス

    Attributes
    ----------
    db : flask_sqlalchemy.SQLAlchemy
        SQLAlchemyのインスタンス
    UserModel : UserModel
        UserModelのクラス
    """

    def __init__(self, app: Flask):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///"user".db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.db = SQLAlchemy(app)

        if not os.exists("./user.db"):
            self.db.create_all()

        class UserModel(self.db.Model):
            """
            ユーザーのモデルクラス

            Parameters
            ----------
            uid : int
                discordユーザーのid
            oauth_token : str
                twitterのoauthのapikey
            oauth_token_secret : str
                twitterのoauthのapikeysecret

            Attributes
            ----------
            uid : int
                discordユーザーのid
            oauth_token : str
                twitterのoauthのapikey
            oauth_token_secret : str
                twitterのoauthのapikeysecret
            """
            uid = self.db.Column(self.db.Integer(17), unique=True)
            oauth_token = self.db.Column(self.db.String(27), unique=True)
            oauth_token_secret = self.db.Column(
                self.db.String(32), unique=True)

            def __init__(self, uid: int, oauth_token: str, oauth_token_secret: str):
                self.uid = uid
                self.oauth_token = oauth_token
                self.oauth_token_secret = oauth_token_secret

        self.UserModel = UserModel

    def add(self, uid: int, oauth_token: str, oauth_token_secret: str):
        user = self.UserModel(uid, oauth_token, oauth_token_secret)
        self.db.add(user)
        self.db.session.commit()

    def read_all(self):
        users = self.UserModel.all()
        return users

    def read_by_uid(self, uid: str):
        user = self.db.session.query(self.UserModel).filter_by(uid=uid).first()
        return user

    def delete(self, uid: int):
        user = self.db.session.query(self.UserModel).filter_by(uid=uid).first()
        self.db.session.delete(user)
        self.db.session.commit()
