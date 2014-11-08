#!/usr/bin/python

import cgi
import os
import random
import datetime

# to facilitate debugging
import cgitb
cgitb.enable()

import sqlite3

form = cgi.FieldStorage()

uN = form['user_name'].value
p_word = form['p_word'].value

def cookiemaker():
	cookie = Cookie.SimpleCookie()
	cookie["session"] = random.randint(0,1000000000)
	cookie["session"]["domain"] = "slerman.rochestercs.org"
	cookie["session"]["path"] = "/"
	expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
	cookie["session"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
	return cookie


codURcookie = os.environ.get('HTTP_COOKIE')

import Cookie


if codURcookie:

	c = Cookie.SimpleCookie(codURcookie)
	conn = sqlite3.connect('users.db')
	cnt = conn.cursor()
	
	for row in cnt.execute('select * from users'):
		
		if int(c["session"].value) == int(row[3]):
			uN = row[0]
	if uN == form['user_name'].value:
		try:
			with conn:
				cnt.execute(('UPDATE users SET logged_in = ? WHERE user_name = ?'), (1, uN))
			conn.commit()
		except sqlite3.IntegrityError:
			pass
		print "Content-type: text/html"
		# don't forget the extra newline!
		print
		print "<html>"
		print "<head><title>Successfully logged in!</title></head>"
		print "<body>"
		print "<h2>You are now logged in as: " + uN + "</h2>"
		print "</body>"
		print "</html>"
	else:
		print "Content-type: text/html"
		# don't forget the extra newline!
		print
		print "<html>"
		print "<head><title>Already logged in!</title></head>"
		print "<body>"
		print "<h2>You are already logged in</h2>"
		print  "<h1> click<a href=""logout.py""> here</a> to log out </h1>"
		print "</body>"
		print "</html>"

else:
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	
	cookie = cookiemaker()
	
	ses_id = int(cookie["session"].value)
	print cookie
	try:
		with conn:
			c.execute(('UPDATE users SET session_id = ? WHERE user_name = ?'), (ses_id, uN))
		conn.commit()
	except sqlite3.IntegrityError:
		pass
		
	for row in c.execute('select user_name from users'):
		if uN == row[0]:
			try:
				with conn:
					c.execute(('UPDATE users SET logged_in = ? WHERE user_name = ?'), (1, uN))
				conn.commit()
			except sqlite3.IntegrityError:
				pass
			log_on = True
			print "Content-type: text/html"
			# don't forget the extra newline!
			print
			print "<html>"
			print "<head><title>Successfully logged in!</title></head>"
			print "<body>"
			print "<h2>You are now logged in as: " + uN + "</h2>"
			print "</body>"
			print "</html>"
	if log_on != True:
			print "Content-type: text/html"
			# don't forget the extra newline!
			print
			print "<html>"
			print "<head><title>Not logged in</title></head>"
			print "<body>"
			print "<h2>There was an error logging in.</h2>"
			print "<h2>Click here to return to the log in page.</h2>"
			print "</body>"
			print "</html>"
			
