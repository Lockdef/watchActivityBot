import discord
from setting import DISCORD_TOKEN


class DiscordBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(presences=True, guild_subscriptions=True, intents=intents)
        self.username = ""

    def set_username(self, username: str):
        self.username = username

    def get_username(self):
        return self.username

    def get_activity(self):
        return self.activity

    async def on_ready(self):
        print("-- LOGINED --")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if self.username == after.display_name:
            self.activity = after.activity
            print(f"{after.display_name}が{before.activity}を辞めて{after.activity}")


if __name__ == '__main__':
    bot = DiscordBot()
    bot.run(DISCORD_TOKEN)
