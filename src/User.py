import sqlite3
from shared import DB_DIR
path = DB_DIR


class User:
    
    @staticmethod
    def add_new(user, coin=0, warn_ctr=0):
        conn = sqlite3.connect(path)
        sql = f"""SELECT ID FROM users WHERE ID = '{str(user.id)}'"""
        c = conn.cursor()
        c.execute(sql)
        if c.fetchone(): 
            return "Already existed user!"
        sql = f"""INSERT INTO users(ID, coin, warn_ctr)
        VALUES ({str(user.id)}, '{coin}', '{warn_ctr}');"""
        c = conn.cursor()
        c.execute(sql)
        conn.commit()

    @staticmethod
    def update_coin(user, coin):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = f"""UPDATE users
        SET coin = {coin} WHERE ID = '{str(user.id)}'
        """
        c.execute(sql)
        conn.commit()

    @staticmethod
    def coin(user):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = f"""SELECT coin FROM users WHERE ID = '{str(user.id)}'"""
        c.execute(sql)
        coin = c.fetchone()[0]
        conn.commit()

        if coin: return coin
        else: return False

    @staticmethod
    def update_warn_ctr(user, warn_ctr):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = f"""UPDATE users
        SET warn_ctr = {warn_ctr} WHERE ID = '{str(user.id)}'
        """
        c.execute(sql)
        conn.commit()

    @staticmethod
    def warn_ctr(user):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = f"""SELECT warn_ctr FROM users WHERE ID = '{str(user.id)}'"""
        c.execute(sql)
        warn_ctr = c.fetchone()[0]
        conn.commit()

        if warn_ctr: return warn_ctr
        else: return False
