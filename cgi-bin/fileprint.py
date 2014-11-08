#!/usr/bin/python

import cgi

import cgitb
cgitb.enable()

form = cgi.FieldStorage()
code = form['code'].value

f = open('data.txt', 'a')
f.write(code)
f.write('\n')
f.close()

all_contents = open('data.txt').read()

print "Content-type: text/html"
print # newline
print all_contents