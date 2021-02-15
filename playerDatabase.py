import sqlite3
import discord
import inspect
import os.path

# if the table isnt created then create it and need only be ran once


def create_player_table():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    print("DB Path :" + path)
    conn = sqlite3.connect(path + '/TheWatcher.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS playerNameChange(playerID INTEGER, originalName TEXT, newName TEXT)')
    conn.commit()
    c.close()
    conn.close()

# add dynamic data to the player table


def add_player_data(playerID, originalName, newName):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    print("DB Path :" + path)
    conn = sqlite3.connect(path + '/TheWatcher.db')
    c = conn.cursor()
    c.execute("INSERT INTO playerNameChange (playerID, originalName, newName) VALUES (?, ?, ?)",
              (playerID, originalName, newName))
    conn.commit()
    c.close()
    conn.close()

# add dynamic data to the player table


def update_player_name(playerID, newName):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    print("DB Path :" + path)
    conn = sqlite3.connect(path + '/TheWatcher.db')
    c = conn.cursor()
    c.execute("UPDATE playerNameChange SET newName =? WHERE playerID = ?",
              (newName, playerID))
    conn.commit()
    c.close()
    conn.close()


def read_existing_player_data():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    print("DB Path :" + path)
    conn = sqlite3.connect(path + '/TheWatcher.db')
    c = conn.cursor()
    players = []
    players = c.execute("SELECT * FROM  playerNameChange").fetchall()
    conn.commit()
    c.close()
    conn.close()
    return players


def check_for_existing_player(playerid):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    print("DB Path :" + path)
    conn = sqlite3.connect(path + '/TheWatcher.db')
    c = conn.cursor()
    players = []
    players = c.execute(
        "SELECT playerID, originalName, newName  FROM  playerNameChange WHERE playerID =?", (playerid,)).fetchall()
    conn.commit()
    c.close()
    conn.close()
    return players


def get_DB_linked_player_Embed_List():
    newList = []
    playerList = read_existing_player_data()
    for p in playerList:
        embed = discord.Embed(title=str(p[1]),
                              url=f"https://steamcommunity.com/profiles/" +
                                  str(p[0]),
                              description='Current Name=' + str(p[2]))
        newList.append(embed)

    return newList
