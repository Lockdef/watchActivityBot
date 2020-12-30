import os
import asyncio
from threading import Thread

from router import app
from settings import DISCORD_TOKEN
from discordBot import DiscordBot

discordBot = DiscordBot()

port = os.environ.get('PORT', 3333)
host = '0.0.0.0'
app_thread = Thread(target=app.run, args=(host, port))
app_thread.start()
loop = asyncio.get_event_loop()
loop.create_task(discordBot.start(DISCORD_TOKEN))
Thread(target=loop.run_forever())
