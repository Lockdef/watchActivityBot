import os
import sqlite3

DB_FILENAME = "user.db"


class UserDB():
    """
    ユーザーに関するデータベース
    twitterのtokenとdiscordのusername、activity_nameを結びつける

    Attributes
    ----------
    connection : sqlite3.Connection
        データベースを表す
    cursor : sqlite3.Cursor
        データベースを操作するカーソル
    """

    def __init__(self):

        isExistedDB = os.path.exists(f"./{DB_FILENAME}")

        self.connction: sqlite3.Connection = sqlite3.connect(DB_FILENAME)
        self.cursor: sqlite3.Cursor = self.connction.cursor()

        if not isExistedDB:
            self.cursor.execute(
                """
                CREATE TABLE user (
                    
                )
                """
            )
