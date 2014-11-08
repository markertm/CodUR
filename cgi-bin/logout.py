#!/usr/bin/python

import cgi
import os
import random
import datetime
# to facilitate debugging
import cgitb
cgitb.enable()

import sqlite3

conn = sqlite3.connect('users.db')
cnt = conn.cursor()

codURcookie = os.environ.get('HTTP_COOKIE')

import Cookie
c = Cookie.SimpleCookie(codURcookie)
for row in cnt.execute('select * from users'):
	if int(row[3]) == int(c['session'].value):
		try:
			with conn:
				cnt.execute(('UPDATE users SET session_id = ?, logged_in = ? WHERE user_name = ?'), (2,0, row[0]))
			conn.commit()
		except sqlite3.IntegrityError:
			pass
		print "Content-type: text/html"
		# don't forget the extra newline!
		print

		print "<html>"
		print "<head><title>Username not avaliable!</title></head>"
		print "<body>"
		print "<h2>You have successfully signed out</h2>"
		print "</body>"
		print "</html>"

