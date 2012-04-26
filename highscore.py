#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

host = "tothemathmos.com"
username = "gigabright"
password = "learningisfun"
databasename = "gigabright"

#NEEDED BUGFIXES:
#-Adding score currently adds multiple entries. Appears to add 2 or 3
#-Retrieving works except for ordering; need that to display best users without ordering within the highscore class
#-INSERT should be changed to REPLACE (I think) but some sort of key must be defined... 
#   Idk too much about mySQL but the same name can be input twice. This resulted in a flood of DStrohl entries on the server =P
#As a side note, limit on score retrieval was removed to access the current user's score position if not in top 10

#Retrieves a list of highscores for a specific game. 
def retrieveHighscores(game):

    rows = False
    con = mdb.connect(host, username, password, databasename);
    
    with con: 

        cur = con.cursor()
        cur.execute("SELECT user, score FROM highscores WHERE game = '" + game + "' ORDER BY score")
        
        rows = cur.fetchall()
        return rows
        
#Adds a new highscore for a specific game. 
def addScore(game, score):
    print "new score"
    success = True

    try:
        player = getPlayer()
        
        con = mdb.connect(host, username, password, databasename);
            
        with con:    

            cur = con.cursor()
            
            query = "INSERT INTO highscores (game, user, score) VALUES (%(game)s, %(user)s, %(score)s)"
            data = {
                'game' : game,
                'user' : player,
                'score' : score
            }
            #print query
            cur.execute(query, data)
    except:
        success = False
    return success

#Reads the player.txt file and returns the players name. 
def getPlayer():
    text = open('player.txt', 'r').read()
    return text
        
#addScore("example.xml", "3000")
#highscores = retrieveHighscores("example.xml")
#for highscore in highscores:
#    print highscore