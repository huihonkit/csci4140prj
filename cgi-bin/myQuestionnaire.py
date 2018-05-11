#! /usr/bin/env python

import cgi
import cgitb
import time
import os
import sqlite3
import urlparse
import subprocess
import Cookie
import math
cgitb.enable()

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<link type="text/css" rel="stylesheet" href="/css/style.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/styleformyQ.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')
	print('<script src="/js/myQ.js"></script>')
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")
'''

def get_uid():
	if 'HTTP_COOKIE' in os.environ:
		cookie_string = os.environ.get('HTTP_COOKIE')
		c = Cookie.SimpleCookie()
		c.load(cookie_string)
		try:
			data = c['csci414064769'].value	
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			c.execute("SELECT uid FROM session WHERE sid = ?", (data,))
			result = c.fetchone()
			conn.close()
			return result[0]
		except:
			return ''

def get_cookie():
	if 'HTTP_COOKIE' in os.environ:
		cookie_string = os.environ.get('HTTP_COOKIE')
		c = Cookie.SimpleCookie()
		c.load(cookie_string)
		try:
			data = c['csci414064769'].value
			error_msg()
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			c.execute("SELECT uid FROM session WHERE sid = ?", (data,))
			result = c.fetchone()
			c.execute("SELECT username FROM user WHERE uid = ?", (result[0],))
			username = c.fetchone()
			conn.close()
			print("<h3>username:" + username[0] + "</h3>")
			update()
			show_image()
			upload()
			logout()
		except:
			error_msg()
			login()
			create()
			show_image()
			upload()
'''
def nav_bar():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
			<a href="createquestion.py">Create Questionnaire</a>
		</div>
		<div class="right">
			<a href="signin.py">Sign in</a>
			<a href="signup.py">Sign up</a>
		</div>
		''')
	print('</div>')

def testboarder():
	print('''
		<br><br>
		<center><h3>Here are all your questionnaires</h3></center>
		<div class="Qblock">
		<h4>Title1</h4>
		</div>
		<br>
		<div class="Qblock">
		<h4>Title2</h4>
		</div>
		<br>
		<div class="Qblock">
		<h4>Title3</h4>
		</div>
		<br>
		''')


htmlTop()
nav_bar()

testboarder()

#get_cookie()
htmlTail()