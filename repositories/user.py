from settings import db
from models.user import UserModel
import sys
sys.path.append('../')


class UserRepository():
    """
    ユーザーデータベースへの操作全般を扱うクラス
    """

    def add(self, uid: int, access_token: str, access_token_secret: str):
        """
        ユーザーを追加する

        Parameters
        ----------
        uid : int
            discordユーザーのid
        access_token : str
            twitterのoauthのapikey
        access_token_secret : str
            twitterのoauthのapikeysecret
        """
        if self.exists(uid):
            self.update(uid, access_token, access_token_secret)
            return
        user = UserModel(uid, access_token, access_token_secret)
        db.session.add(user)
        db.session.commit()

    def read_all(self):
        """
        ユーザーデータを全て取得する
        """
        users = UserModel.all()
        return users

    def read_by_uid(self, uid: str):
        """
        uidが一致するユーザーデータを取得する

        Parameters
        ----------
        uid : int
            discordユーザーのid
        """
        user = db.session.query(UserModel).filter_by(uid=uid).first()
        return user

    def delete(self, uid: int):
        """
        uidが一致するユーザーデータを削除する

        Parameters
        ----------
        uid : int
            discordユーザーのid
        """
        user = db.session.query(UserModel).filter_by(uid=uid).first()
        db.session.delete(user)
        db.session.commit()

    def exists(self, uid: int) -> bool:
        """
        uidが一致するユーザーデータが存在するか真偽値を取得する

        Parameters
        ----------
        uid : int
            discordユーザーのid

        Returns
        -------
        isExists : bool
            存在するかの真偽値
        """
        isExists = db.session \
            .query(UserModel) \
            .filter_by(uid=uid) \
            .scalar() \
            is not None
        return isExists

    def update(self, uid: int, access_token: str, access_token_secret: str):
        """
        tokenを更新する

        Parameters
        ----------
        uid : int
            discordユーザーのid
        access_token : str
            twitterのoauthのapikey
        access_token_secret : str
            twitterのoauthのapikeysecret
        """
        user = db.session.query(UserModel).filter_by(uid=uid).first()
        user.access_token = access_token
        user.access_token_secret = access_token_secret
        db.session.add(user)
        db.session.commit()
