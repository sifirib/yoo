import datetime
from asyncio import sleep
from discord.ext import tasks

class Bump():
    active = True

    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel = self.bot.fetch_channel(channel_id)


    async def pause_(self):
        self.active = False
        print("Bump paused.")

    async def continue_(self):
        self.active = True
        print("Bump restored.")

    @tasks.loop(seconds=5) # task runs every 60 seconds
    async def check_(self):
        message = await self.channel.history(limit=1)
        print(message)
        print(dir(message))
        if str(message.author) == "DISBOARD#2760":
            if "Bump Done" in message.embeds[0].description:
                now = datetime.datetime.utcnow()
                two = datetime.timedelta(hours=2)
                min_ = datetime.timedelta(minutes=1)

                diff = now - message.created_at
                diff = two - diff + min_
                print(f"Time until next bump {diff}")

                return diff.seconds
    @check_.before_loop
    async def before_check_(self):
        await self.bot.wait_until_ready() # wait until the bot logs in
                

    async def bump_(self):
        print(self.channel)
        print(dir(self.channel))
        self.diff = await self.check_()
        await sleep(self.diff)
        command = await self.channel.send("!d bump")
        print("Server bumped.")

        return command


    
