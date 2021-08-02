import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, "databases/", "deneme.db")

# CFG_DIR = os.path.join(ROOT_DIR, "utils/", "config.json")

keycap_digits = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
hangman_body = ["""
__________
|    │
|   😵
|  ┌()┐
|   〈 〉
|""", """
__________
|    │
|   😵
|  ┌()┐
|   〈
|""", """
__________
|    │
|   😵
|  ┌()┐
|
|""", """
__________
|    │
|   😵
|  ┌()
|
|""", """
__________
|    │
|   😵
|   ()
|
|""", """
__________
|    │
|   😵
|   (
|
|""", """
__________
|    │
|   😵
|   
|
|""", """
__________
|    │
|    
|
|"""]

f = open("src/wordlist.txt", "r")
words = [line.strip() for line in f.readlines()]
f = open("src/badwords.txt", "r")
badwords = [line.strip() for line in f.readlines()]

def check_reaction(ctx, reaction, user):
    return user == ctx.author and str(reaction.emoji) in keycap_digits