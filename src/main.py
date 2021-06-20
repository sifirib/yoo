import discord
import time
from discord import file
from discord import channel
from discord import message
from discord import embeds
from discord import utils
from discord.ext import commands
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
async def av(ctx, *, avamember:discord.Member=None):
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
    if args[0] == 'start':  
        game.start_game()
        game_message = 'A word has been randomly selected (all lowercase). \nGuess letters by using `.hangman x` (x is the guessed letter). \n'
    else:
        # print(dir(ctx.message))
        print(ctx.message.content)
        game.guess(ctx.message.content)
    print(game.remaining_guesses)
    await ctx.channel.send(game_message, embed=game.create_embed(hangman_body[game.remaining_guesses - 1]))



# Connect 4
@bot.command()
async def test(ctx):
    
    message = await ctx.send('test')
    # emoji = '\N{ONE SIGN}'
    reactions = keycap_digits
    for r in reactions:
        await message.add_reaction(r)
    
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
    print(last_bot_msg.content)

    if message.id != last_bot_msg.id: return

    try:
        game_info = games[user.id]
    except KeyError:
        await channel.send("You are not currently in a game " + user.mention)
        await reaction.remove(user)
        return
    # if game_info['game'].turn == game_info['team']:
    #     if reaction.emoji in keycap_digits: return keycap_digits.index(reaction.emoji)
    
       
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
                await channel.send("You must give a valid column " + message.author.mention)
            
            elif winner:
                file_name = str(message.author.id) + ".png"
                
                if game_info["team"] == 0:
                    pc = colors.get(message.author, "red")
                    oc = colors.get(game_info['opponent'], "black")
                    game_info['game'].generateImageBoard(pc, oc).save(file_name, "PNG")
                else:
                    pc = colors.get(message.author, "black")
                    oc = colors.get(game_info['opponent'], "red")
                    game_info['game'].generateImageBoard(oc, pc).save(file_name, "PNG")

                new_board = await channel.send(file=discord.File(file_name), content=message.author.mention + " won!")
                for r in keycap_digits:
                    await new_board.add_reaction(r)
                opp_id = game_info['opponent'].id

                del games[opp_id]
                del games[message.author.id]

            else:
                file_name = str(message.author.id) + ".png"

                if game_info["team"] == 0:
                    pc = colors.get(message.author, "red")
                    oc = colors.get(game_info['opponent'], "black")
                    game_info['game'].generateImageBoard(pc, oc).save(file_name, "PNG")
                else:
                    pc = colors.get(message.author, "black")
                    oc = colors.get(game_info['opponent'], "red")
                    game_info['game'].generateImageBoard(oc, pc).save(file_name, "PNG")

                new_board = await channel.send("Your turn " + user.mention, file=discord.File(file_name))
                for r in keycap_digits:
                    await new_board.add_reaction(r)

        else:
            await channel.send("You must give a valid column " + message.author.mention)






bot.run(TOKEN)

