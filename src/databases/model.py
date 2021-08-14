from orm import Model
from orm import Database
from datetime import datetime
import os
import psycopg2

# DATABASE_URL = os.environ['DATABASE_URL']


# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
class Person(Model):

    discord_id = int
    coin = int
    warn_ctr = int
    # first_join_date = str


    def __init__(self, discord_id, coin, warn_ctr):
        self.discord_id = discord_id
        self.coin = coin
        # self.first_join_date = first_join_date
        self.warn_ctr = warn_ctr



def get_user(discord_id):
    objects = Person.manager(db)
    users = list(objects.all())
    
    for user in users:
        if user.discord_id == discord_id: return user

    return False


db = Database("src/databases/member.sqlite")
Person.db = db