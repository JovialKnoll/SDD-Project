#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

def retrieveHighscores(game):
	con = mdb.connect('localhost', 'root', 
			'', 'gigabright');

	with con: 

		cur = con.cursor()
		cur.execute("SELECT user, score FROM highscores WHERE game = '" + game + "' ORDER BY score DESC LIMIT 10")
		
		rows = cur.fetchall()
		return rows
		
def addScore(game, user, score):
	con = mdb.connect('localhost', 'root', 
		'', 'gigabright')
		
	with con:    

		cur = con.cursor()
		query = "INSERT INTO highscores (game, user, score) VALUES ('" + game + "', '" + user + "', '" + score + "')"
		#print query
		cur.execute(query)
		
		#print "Number of rows updated: %d" % cur.rowcount

#addScore("example.xml", "bran", "3000")
#highscores = retrieveHighscores("example.xml")
#for highscore in highscores:
#	print highscore