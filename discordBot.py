import discord
from setting import DISCORD_TOKEN


class DiscordBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(presences=True, guild_subscriptions=True, intents=intents)
        self.usernames = set()
        self.activity_name = None

    def add_username(self, username: str):
        self.usernames.add(username)

    def get_username(self):
        return self.username

    def get_activity(self):
        return self.activity_name

    async def on_ready(self):
        print("-- LOGINED --")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.display_name in self.usernames:
            if after.activity is None:
                self.activity_name = "None"
                print(f"{after.display_name}がアクティビティを終了")
                return
            self.activity_name = after.activity.to_dict()['name']
            print(f"{after.display_name}がアクティビティ{self.activity_name}を開始")


if __name__ == '__main__':
    bot = DiscordBot()
    bot.run(DISCORD_TOKEN)
