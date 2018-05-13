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

myusername = ""
myuserid = -1

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

def get_cookie():
	global myusername, myuserid
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
			if result is not None:
				c.execute("SELECT uname FROM user WHERE uid = ?", (result[0],))
				myuserid = result[0]
				username = c.fetchone()
				nav_bar2(username[0])
				myusername = username[0]
			else:
				nav_bar1()
			conn.close()
		except:
			nav_bar1()

def nav_bar1():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="search.py">Search</a>
		</div>
		<div class="right">
			<a href="login.py">Sign in</a>
			<a href="signup.py">Sign up</a>
		</div>
		''')
	print('</div>')


def nav_bar2(uname):
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
			<a href="createquestion.py">Create Questionnaire</a>
		</div>
		<div class="right">''')
	print("<a>"+uname+"</a>")
	print('''
			<a href="logout.py">Logout</a>
		</div>
		''')
	print('</div>')

def body():
	print('''
		<br><br>
		<center><h3>Here are all your questionnaires, %s</h3></center>
		''') % (myusername)
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select mark from user where uid=%d' % (myuserid)) 
	temp = c.fetchone()
	maxmk = temp[0]
	c.execute('select * from question where uid=%d' % (myuserid)) 
	Qs = c.fetchall()
	for row in Qs:
		print('<div><a href="http://localhost:8080/cgi-bin/Qstat.py?targetQ=%d" style="text-decoration : none; color : #000000;"><div class="Qblock"><i>&nbsp;&nbsp;%s</i>&nbsp;&nbsp;&nbsp;&nbsp;%d people done, used %d marks<br><span style="font-size:24px">&nbsp;&nbsp;%s</span></div></a><div class="stat"><form action="/cgi-bin/myQuestionnaire.py" method="get" id="changemk"><label for="user_lic">Add marks to the above questionnaire: </label><input id="user_lic" type="number" name="addmk" min="0" max="%d" step="1" value ="0"/></form><button type="submit" form="changemk" value="Submit">Submit</button></div></div><br>' % (row[0], row[7], row[9], row[3], row[5], maxmk))



htmlTop()
get_cookie()

body()

#get_cookie()
htmlTail()