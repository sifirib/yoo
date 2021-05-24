import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import bot_has_role
from utils import *
from youtubesearchpython import VideosSearch
import time
from Games.tiny_games import *
from Games.Hangman import Hangman
from Games.connect4 import Game, Board



intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=".l ", intents=intents)

# game = Game()
game = Hangman()

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="gelen-giden")
    await channel.send(f"Hos geldin {member} c:")
    print(f"Hos geldin {member} c:")

# @bot.command(pass_context=True)
# async def ping(ctx):
#     await ctx.send(f'{round(bot.latency * 1000)} ms')
@bot.command(pass_context=True)
async def ping(ctx):
        time_1 = time.perf_counter()
        await ctx.trigger_typing()
        time_2 = time.perf_counter()
        ping = round((time_2-time_1) * 1000)
        await ctx.send(f"{ping} ms")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount:int=1):
    await ctx.channel.purge(limit = amount + 1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to do that!")


@bot.command(aliases=["copy"])
async def clone_channel(ctx, amount=1):
    print(ctx.channel)
    for i in range(amount):
        await ctx.channel.copy()


@bot.command(aliases=["oyun"])
async def deneme(ctx, *args):
    print(dir(ctx.channel))
    if "roll" in args:
        await ctx.send(game.roll_dice())
    else:
        await ctx.send("yee")


@bot.command()
async def av(ctx, *, avamember:discord.Member=None):
    user_avatar_url = avamember.avatar_url

    await ctx.send(user_avatar_url)


@bot.command(aliases=["yt"])
async def ytplay(ctx, *args:str):

    base = "https://www.youtube.com/results?search_query="
    query = args
    search_url = base + '+'.join(query)

    videos_search = VideosSearch(search_url, limit=1)
    results = videos_search.result()["result"][0]
    url_of_music = results["link"]
    view_count = results["viewCount"]["short"]
    published_time = results["publishedTime"]
    # print(url_of_music)

    await ctx.send(f":globe_with_meridians: {view_count} :cyclone: {published_time}\n{url_of_music}")
    
    



@bot.command()
async def hangman(ctx, *args:str):
    # elif message.content.startswith('!hangman'):
    game_message = ""
    if args[0] == 'start':
        game.start_game()
        game_message = 'A word has been randomly selected (all lowercase). \nGuess letters by using `!hangman x` (x is the guessed letter). \n'
    else:
        # print(dir(ctx.message))
        print(ctx.message.content)
        game.guess(ctx.message.content)
    
    await ctx.channel.send(game_message + game.get_game_status())














bot.run(TOKEN)

