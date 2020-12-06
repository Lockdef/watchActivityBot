import discord
from setting import TOKEN


class DiscordBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(presences=True, guild_subscriptions=True, intents=intents)

    async def on_ready(self):
        print("-- LOGINED --")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        print(f"{after.display_name}が{before.activity}を辞めて{after.activity}")


if __name__ == '__main__':
    bot = DiscordBot()
    bot.run(TOKEN)
