#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

host = "tothemathmos.com"
username = "gigabright"
password = "learningisfun"
databasename = "gigabright"

def retrieveHighscores(game):
	con = mdb.connect(host, username, password, databasename);

	with con: 

		cur = con.cursor()
		cur.execute("SELECT user, score FROM highscores WHERE game = '" + game + "' ORDER BY score DESC LIMIT 10")
		
		rows = cur.fetchall()
		return rows
		
def addScore(game, score):
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
		
		#print "Number of rows updated: %d" % cur.rowcount

def getPlayer():
	text = open('player.txt', 'r').read()
	return text
		
#addScore("example.xml", "3000")
#highscores = retrieveHighscores("example.xml")
#for highscore in highscores:
#	print highscore