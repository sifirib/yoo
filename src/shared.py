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

def check_reaction(ctx, reaction, user):
    return user == ctx.author and str(reaction.emoji) in keycap_digits
