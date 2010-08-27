#!/usr/bin/python

'''
Posty
Written by Nick Pegg
http://nickpegg.com/

Very simple static blog engine. 
Takes in markdown files, spits out a website.
Invoked via command line with a few commands.
'''

import os
import sys
import shutil

import sqlite3
import markdown


def init():
	""" Initialize the blog. Create directories, database, etc. """
	
	try:
		open('posts.db')
		print("Uh-oh! Looks like you already have a posts database.")
		print("Reinitializing will destroy EVERYTHING. Chiggity-check yourself before you wreck yourself.")
		response = raw_input("Type YES if you really want to do re-initialize: ")
		
		if response != "YES":
			print("\nYou didn't type YES, so I'm not doing to do anything.")
			quit()
		print("\nAlright then. I'm giving you a blank slate now.")
	except IOError:
		pass
	
	print("\nInitializing your blog...")
	
	# Init the database
	sql_conn = sqlite3.connect("posts.db")
	cursor = sql_conn.cursor()
	cursor.execute('drop table if exists posts')
	cursor.execute('''create table posts (id integer primary key 
					autoincrement, title text, date text, 
					body text)''')
					
	shutil.rmtree("output", ignore_errors=True)
	
def post():
	""" Add a new post to the database """
	pass
	
def list():
	""" Lists all of the posts in the database """
	cursor = sqlite3.connect("posts.db").cursor()
	cursor.execute("select * from posts")
	
	if cursor.rowcount == -1:
		print("There are no posts.")
		quit()
		
	print("ID\tPost Title")
	print("----------------")
	for row in cursor:
		print(str(row['id']) + "\t" + row['title'])
		
	print("\nIf you would like to remove a post, do it like so:")
	print("posty.py rm [id] \nWhere [id] is the post id seen above.")
	
def rm(args):
	""" Remove a post from the database """
	try:
		id = long(args[0])
	except:
		print('''You supplied an id that's not a number! Find a suitable one 
				via the list command.''')
	
	cursor = sqlite3.connect("posts.db").cursor()
	cursor.execute("delete from posts where id = ?", id)
	
	if cursor.rowcount < 1:
		print("I couldn't find the row you're talking about. Check to see if it exists by using the list command.")
	else:
		print("Successfully deleted post #" + str(id) + "!")
	
def render(args):
	""" Render the posts and pages into a bunch of HTML files """
	pass

def main():
	try:
		cmd = sys.argv[1]
	except:
		print("You need to specify a command.")
		print("Valid commands include: init, post, list, rm, render")
		quit(-1)
		
	args = sys.argv[2:]
	
	if cmd == "init":
		init()
	elif cmd == "list":
		list()
	elif cmd == "rm":
		rm(args)
	else:
		print("\n\nInvalid command!")
	

if __name__ == "__main__":
	main()