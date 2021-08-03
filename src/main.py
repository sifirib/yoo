from os import sched_getaffinity
import discord
import time
import asyncio
from discord import file
from discord import channel
from discord import message
from discord import embeds
from discord import utils
from discord.ext import commands
from discord.gateway import DiscordWebSocket
from User import User
from utils.utils import *
from youtubesearchpython import VideosSearch
from Games.tiny_games import *
from Games.Hangman import Hangman
from Games.connect4.Game import Game
from shared import *

games = {}
colors = {}

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=".", intents=intents)

# game = Game()
game = Hangman()
board_message_history = []

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("Ready!")
    print("------")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="gelen-giden")
    User.add_new(member, 100, 3)
    print(User.coin(member))
    print(User.warn_ctr(member))
    await channel.send(f"Hos geldin {member.mention} c:")
    print(f"Hos geldin {member.mention} c:")

@bot.event
async def on_profanity(message, word):
    warn_ctr = User.warn_ctr(message.author)
    User.update_warn_ctr(message.author, warn_ctr + 1)
    channel = message.channel
    embed = discord.Embed(title="WARNING!", 
    description=f"{message.author.name} just said ||{word}||\n You have been warned **{warn_ctr}** times.", color=discord.Color.blurple())
    
    if User.warn_ctr(message.author) >= 3:
        duration = 10
        unit = "s"
        roleobject = discord.utils.get(message.guild.roles, id=863562272668385311)
        await channel.send(f":white_check_mark: Muted {message.author} for {duration}{unit}")
        await message.author.add_roles(roleobject)
        # await channel.set_permissions(message.author, send_messages=False)
        if unit == "s":
            wait = 1 * duration
            await asyncio.sleep(wait)
        elif unit == "m":
            wait = 60 * duration
            await asyncio.sleep(wait)

        await message.author.remove_roles(roleobject)
        # await channel.set_permissions(message.author, send_messages=True)
        await channel.send(f":white_check_mark: {message.author} was unmuted") 



    await channel.send(embed=embed)


# @bot.event
# async def on_member_update(before, after):
#     # text_channel_list = []
#     # for guild in bot.guilds:
#     #     for channel in guild.text_channels:
#     #         text_channel_list.append(channel)
#     # last_msg = None
#     # for channel in text_channel_list:
#     #     aux = await channel.history(limit=1).find(lambda m: m.author.id == after.user.id)
#     #     if aux.created_at > last_msg.created_at:
#     #         last_msg = aux


#     # channel = discord.utils.get(after.guild.text_channels, name="bot")
#     text_channel_list = []
#     for guild in bot.guilds:
#         for channel in guild.text_channels:
#             text_channel_list.append(channel)
#     for channel in text_channel_list:
#         for role in after.roles:
#             if role.name == "Muted":
#                 await channel.set_permissions(after, send_messages=False)
#                 return
#         await channel.set_permissions(after, send_messages=True)


# @bot.event
# async def on_message(message):
#     # last_message = await message.author.history(limit=1).flatten()[0]
#     # history = await message.author.history(limit=1)
#     # history_listesi = await history.flatten()
#     # last_message = history_listesi[0]
#     # print(last_message)
#     # print(dir(message.author.history))
#     # print(type(message.created_at))
#     # print(message.author.history)


#     for i in badwords:
#         if i in message.content:
#             await message.delete()
#             await message.channel.send(f"{message.author.mention} Don't use that word!")
#             bot.dispatch("profanity", message, i)
#             return # So that it does not try to delete the message again, which will cause an error.

#         await bot.process_commands(message)




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
@commands.has_permissions(kick_members=True)
async def mute(ctx, user : discord.Member, duration = 0,*, unit = None):
    roleobject = discord.utils.get(ctx.message.guild.roles, id=730016083871793163)
    await ctx.send(f":white_check_mark: Muted {user} for {duration}{unit}")
    await user.add_roles(roleobject)
    if unit == "s":
        wait = 1 * duration
        await asyncio.sleep(wait)
    elif unit == "m":
        wait = 60 * duration
        await asyncio.sleep(wait)
    await user.remove_roles(roleobject)
    await ctx.send(f":white_check_mark: {user} was unmuted") 

@bot.command()
@commands.has_permissions(administrator=True)
# @commands.has_role(840869771356012555)
async def clear(ctx, amount:int=1):
    await ctx.channel.purge(limit = amount + 1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to do that!")

@bot.command(aliases=["copy"])
@commands.has_permissions(administrator=True)
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
async def av(ctx, *, avamember: discord.Member=None):
    user_avatar_url = avamember.avatar_url

    await ctx.send(user_avatar_url)


@bot.command(aliases=["yt"])
async def ytplay(ctx, *args:str):

    base = "https://www.youtube.com/results?search_query="
    query = args
    search_url = base + '+'.join(query)
    print(search_url)
    videos_search = VideosSearch(search_url, limit=5)
    print(videos_search.result())
    results = videos_search.result()["result"][0]
    url_of_music = results["link"]
    view_count = results["viewCount"]["short"]
    published_time = results["publishedTime"]
    # print(url_of_music)

    await ctx.send(f":globe_with_meridians: {view_count} :cyclone: {published_time}\n{url_of_music}")
    


@bot.command(aliases=["hm"])
async def hangman(ctx, *args:str):
    # elif message.content.startswith('!hangman'):
    game_message = ""
    author = ctx.author
    if args[0] == 'start':
        # User.add_new(author)
        print(author.id)
        User.coin(author)
        game.start_game(author)
        game_message = 'A word has been randomly selected (all lowercase). \nGuess letters by using `.hangman x` (x is the guessed letter). \n'
    else:
        # print(dir(ctx.message))
        User.coin(author)
        print(ctx.message.content)
        game.guess(ctx.message.content)
    print(game.remaining_guesses)
    await ctx.channel.send(game_message, embed=game.create_embed(hangman_body[game.remaining_guesses - 1]))


# Connect 4
@bot.command(aliases=["c4"])
async def connect4(ctx, *args:str):

    # print(dir(ctx.message.content))
    message = ctx.message
    print(message.content)
    if args[0] == "color":
        ind = message.content.find("#")
        print("ind: ", ind)
        if ind > -1:
            color = message.content[ind:]
            colors[message.author] = color
            await ctx.channel.send("Color has set.")
        else:
            await ctx.channel.send("Colors must be set as hex!")
        print(colors[ctx.author])

    elif args[0] == "resign":
        try:
            game_info = games[message.author.id]
        except KeyError:
            await ctx.channel.send("You are not currently in a game " + message.author.mention)
            return

        opp_id = game_info['opponent'].id

        del games[opp_id]
        del games[message.author.id]

    elif args[0] == "start":
        player = message.author
        opponent = message.mentions[0]

        if player in games or opponent in games:
            await ctx.channel.send("One of you is already in another game!")
            return

        game = Game()
        games[player.id] = {"game": game, "opponent": opponent, "team": 0}
        games[opponent.id] = {"game": game, "opponent": player, "team": 1}
        # await ctx.channel.send("`" + str(games[message.author]['game']) + "`")

        file_name = str(player.id) + ".png"
        
        game.generateImageBoard().save(file_name, "PNG")
        
        new_board = await ctx.send("Your turn " + player.mention, file=discord.File(file_name))
        for r in keycap_digits:
            await new_board.add_reaction(r)



@bot.event
async def on_reaction_add(reaction, user):
    if user.id == bot.user.id: return

    message = reaction.message
    channel = message.channel
    last_bot_msg = await channel.history(limit=1).find(lambda m: m.author.id == bot.user.id)
    if not last_bot_msg: return
    print(last_bot_msg.content)

    if message.id != last_bot_msg.id: return

    try:
        game_info = games[user.id]
    except KeyError:
        await channel.send("You are not currently in a game " + user.mention)
        await reaction.remove(user)
        return

       
    if game_info['game'].turn != game_info['team']:
        await reaction.remove(user)
        return
    else:
        if reaction.emoji in keycap_digits:
            column = str(keycap_digits.index(reaction.emoji))
        else:
            return

        if column.isdigit() and int(column) >= 0 and int(column) < 7:
            winner = game_info['game'].move(int(column))
            if winner == -1:
                await channel.send("You must give a valid column " + user.mention)
                return

            elif winner:
                file_name = str(user.id) + ".png"
                
                if game_info["team"] == 0:
                    pc = colors.get(user, "red")
                    oc = colors.get(game_info['opponent'], "black")
                    game_info['game'].generateImageBoard(pc, oc).save(file_name, "PNG")
                else:
                    pc = colors.get(user, "black")
                    oc = colors.get(game_info['opponent'], "red")
                    game_info['game'].generateImageBoard(oc, pc).save(file_name, "PNG")

                new_board = await channel.send(file=discord.File(file_name), content=user.mention + " won!")
                for r in keycap_digits:
                    await new_board.add_reaction(r)
                opp_id = game_info['opponent'].id

                del games[opp_id]
                del games[user.id]

            else:
                file_name = str(user.id) + ".png"

                if game_info["team"] == 0:
                    pc = colors.get(user, "red")
                    oc = colors.get(game_info['opponent'], "black")
                    game_info['game'].generateImageBoard(pc, oc).save(file_name, "PNG")
                else:
                    pc = colors.get(user, "black")
                    oc = colors.get(game_info['opponent'], "red")
                    game_info['game'].generateImageBoard(oc, pc).save(file_name, "PNG")

                new_board = await channel.send("Your turn " + game_info["opponent"].mention, file=discord.File(file_name))
                for r in keycap_digits:
                    await new_board.add_reaction(r)

        else:
            await channel.send("You must give a valid column " + game_info["opponent"].mention)






if __name__ == "__main__":
    bot.run(TOKEN)

