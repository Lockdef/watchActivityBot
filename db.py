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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.db = SQLAlchemy(app)

        class UserModel(self.db.Model):
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
            uid = self.db.Column(self.db.Integer(), primary_key=True)
            access_token = self.db.Column(self.db.String(27), unique=True)
            access_token_secret = self.db.Column(
                self.db.String(32), unique=True)

            def __init__(self, uid: int, access_token: str, access_token_secret: str):
                self.uid = uid
                self.access_token = access_token
                self.access_token_secret = access_token_secret

        if not os.path.exists("./user.db"):
            self.db.create_all()

        self.UserModel = UserModel

    def add(self, uid: int, access_token: str, access_token_secret: str):
        if self.exists(uid):
            self.update(uid, access_token, access_token_secret)
        user = self.UserModel(uid, access_token, access_token_secret)
        self.db.session.add(user)
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

    def exists(self, uid: int) -> bool:
        isExists = self.db.session \
            .query(self.UserModel) \
            .filter_by(uid=uid) \
            .scalar() \
            is not None
        return isExists

    def update(self, uid: int, access_token: str, access_token_secret: str):
        user = self.db.session.query(self.UserModel).filter_by(uid=uid).first()
        user.access_token = access_token
        user.access_token_secret = access_token_secret
        self.db.session.add(user)
        self.db.session.commit()
