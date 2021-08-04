import asyncio
from typing import AsyncIterable
import discord, datetime
from asyncio import sleep

from discord import channel

class Bump():
    active = True

    def __init__(self, channel_id):
        self.channel = self.get_channel(channel_id)

    async def pause_(self):
        self.active = False
        print("Bump paused.")

    async def continue_(self):
        self.active = True
        print("Bump restored.")

    async def check_(self):
        async for message in self.channel.history(limit=50):
            if str(message.author) == "DISBOARD#2760":
                if "Bump Done" in message.embeds[0].description:
                    now = datetime.datetime.utcnow()
                    two = datetime.timedelta(hours=2)
                    min_ = datetime.timedelta(minutes=1)

                    diff = now - message.created_at
                    diff = two - diff + min_
                    print(f"Time until next bump {diff}")

                    return diff.seconds
                    break

    async def bump_(self):
        self.diff = await self.check_()
        await sleep(self.diff)
        command = await self.channel.send("!d bump")
        print("Server bumped.")

        return command

    
    
