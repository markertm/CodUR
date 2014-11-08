#!/usr/bin/python

import cgi

import cgitb
cgitb.enable()

all_contents = open('data.txt').read()

print "Content-type: text/html"
print # newline
print all_contents