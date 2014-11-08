#!/usr/bin/python

import cgi

# to facilitate debugging
import cgitb
cgitb.enable()

import sqlite3

form = cgi.FieldStorage()

user_name = form['user_name'].value
p_word = form['p_word'].value
e_mail = form['e_mail'].value
avaliable = True;

conn = sqlite3.connect('users.db')
c = conn.cursor()

for row in c.execute('select user_name from users'):
	if user_name == row[0]:
		print "Content-type: text/html"
		# don't forget the extra newline!
		print

		print "<html>"
		print "<head><title>Username not avaliable!</title></head>"
		print "<body>"
		print "<h2>The Username you have selected is already in use</h2>"
		print "<h3>Click here to return to sign up.</h3>"
		avaliable = False;
		
if 	avaliable:	
	try:
		c.execute('insert into users values(?,?,?,2,0 );', (user_name, p_word, e_mail))
		conn.commit()
	except sqlite3.IntegrityError:
		pass
		

	print "Content-type: text/html"
	# don't forget the extra newline!
	print

	print "<html>"
	print "<head><title>Welcome to CodUR!</title></head>"
	print "<body>"
	print "<h1> Welcome to CodUR!</h1>"
	print "<h2>Your Username is: " + form['user_name'].value + "</h2>"
	print "<h2>Your Password is: " + form['p_word'].value + "</h2>"
	print "<h2>The E-mail you used to sign up is: " + form['e_mail'].value + "</h2>"

	print "</body>"
	print "</html>"
