
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
TOKEN = os.getenv("DISCORD_TOKEN")



# def get_user(guild, arg):
#     # guild -> discord.Guild
#     # arg   -> user mention string
#     # arg   -> user ID
#     # arg   -> username / username#discriminator

#     if isinstance(arg, discord.User) or isinstance(arg, discord.Member):
#         return arg

#     else:
#         if arg.startswith("<@!") or arg.startswith("<@"):
#             s = ""
#             for char in str(arg):
#                 if char.isdigit(): s += char

#             user = guild.get_member(int(s))
#             if user: return user

#         try:
#             user = guild.get_member(int(arg))
#             if user: return user

#         except:
#             argl = arg.lower()
#             for member in guild.members:
#                 if member.name.lower() == argl or str(member).lower() == argl or argl in member.name.lower() or member.display_name.lower() == argl or argl in member.display_name.lower():
#                     return member

#                 if member.nick:
#                     if member.nick.lower() == argl or argl in member.nick.lower():
#                         return member