import discord
from setting import DISCORD_TOKEN


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
        self.usernames = set()
        self.activity_name = {}

    def add_username(self, username: str, tag: str):
        """
        監視対象のユーザーを追加する

        Parameters
        ----------
        username : str
            追加するユーザー名
        tag : str
            追加するユーザーの4桁の整数で構成されるタグ
        """
        user = f"{username}#{tag}"
        self.usernames.add(user)
        self.activity_name[user] = "None"

    def get_activity(self, username: str, tag: str) -> str:
        """
        対象のユーザーのアクティビティ名を取得する

        Parameters
        ----------
        username : str
            アクティビティ名を取得したいユーザー名
        tag : str
            追加するユーザーの4桁の整数で構成されるタグ

        Returns
        -------
        activity_name : str
            対象のユーザーのアクティビティ名
        """
        user = f"{username}#{tag}"
        activity_name = self.activity_name[user]
        return activity_name

    async def on_ready(self):
        """
        起動時に実行される関数
        """
        print("-- LOGINED --")

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
        user = f"{after.name}#{after.discriminator}"
        if user in self.usernames:
            if after.activity is None:
                self.activity_name[user] = "None"
                print(f"{user}がアクティビティを終了")
                return
            self.activity_name[user] = after.activity.to_dict()['name']
            print(
                f"{user}がアクティビティ{self.activity_name[user]}を開始")


if __name__ == '__main__':
    bot = DiscordBot()
    bot.run(DISCORD_TOKEN)
