import discord
from twitterApp import TwitterApp
from repositories.user import UserRepository

user = UserRepository()
twitterApp = TwitterApp()


class DiscordBot(discord.Client):
    """
    Discord関連の処理を行う

    Attributes
    ----------
    usernames : set
        監視対象のユーザー名の集合
    activity_name : dict
        ユーザーごとのアクティビティ名
    """

    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(presences=True, guild_subscriptions=True, intents=intents)

    async def on_ready(self):
        """
        起動時に実行される関数
        """
        print("-- LOGINED --")

    async def on_message(self, message: discord.Message):
        """
        メンションされた時に実行される関数
        DMにidを送信する

        Parameters
        ----------
        message : discord.Message
            メッセージに関する情報
        """
        if message.author.bot:
            return
        dm = await message.author.create_dm()
        await dm.send(f"あなたのidは\n`{message.author.id}`")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """
        メンバーに変化があったときに実行される関数
        activity_nameを更新する

        Parameters
        ----------
        before : discord.Member
            変更前のメンバー情報
        after : discord.Member
            変更後のメンバー情報
        """
        uid: int = after.id

        if not user.exists(uid):
            return

        if after.activity is None:
            activity = "None"
            print(f"{uid}がアクティビティを終了")
        else:
            activity: str = after.activity.to_dict()['name']
            print(f"{uid}がアクティビティ{activity}を開始")

        print(twitterApp.update_profile(uid, activity))
