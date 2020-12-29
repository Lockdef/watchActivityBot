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
            api_key : str
                twitterのoauthのapikey
            api_key_secret : str
                twitterのoauthのapikeysecret

            Attributes
            ----------
            uid : int
                discordユーザーのid
            api_key : str
                twitterのoauthのapikey
            api_key_secret : str
                twitterのoauthのapikeysecret
            """
            uid = self.db.Column(self.db.Integer(17), unique=True)
            api_key = self.db.Column(self.db.String(27), unique=True)
            api_key_secret = self.db.Column(self.db.String(32), unique=True)

            def __init__(self, uid: int, api_key: str, api_key_secret: str):
                self.uid = uid
                self.api_key = api_key
                self.api_key_secret = api_key_secret

        self.UserModel = UserModel

    def add(self, uid: int, api_key: str, api_key_secret: str):
        user = self.UserModel(uid, api_key, api_key_secret)
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
