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
	global myuserid, myusername
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
				myuserid = result[0]
				c.execute("SELECT uname, mark FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				myusername = username[0]
				nav_bar2(username[0], username[1])
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


def nav_bar2(uname, mark):
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
			<a href="createquestion.py">Create Questionnaire</a>
			<a href="myDraft.py">My Draft</a>
		</div>
		<div class="right">''')
	print("<a>"+uname+"</a>")
	print("<a>Mark:"+str(mark)+"</a>")
	print('''
			<a href="logout.py">Logout</a>
		</div>
		''')
	print('</div>')

def checkpost():
	form = cgi.FieldStorage()
	if form:
		target = int(form.getvalue('addmktarget'))
		targetaddmk = int(form.getvalue('addmk'))
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		c.execute('select use_mark from question where qid=%d' % (target))
		tempmark = c.fetchone()
		newmk = tempmark[0] + targetaddmk
		c.execute('update question set use_mark=%d where qid=%d' % (newmk, target))
		conn.commit()

		c.execute('select mark from user where uid=%d' % (myuserid))
		tempumark = c.fetchone()
		newumk = tempumark[0] - targetaddmk
		c.execute('update user set mark=%d where uid=%d' % (newumk, myuserid))
		conn.commit()

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
		print('<div><a href="http://localhost:8080/cgi-bin/Qstat.py?targetQ=%d" style="text-decoration : none; color : #000000;"><div class="Qblock"><i>&nbsp;&nbsp;%s</i>&nbsp;&nbsp;&nbsp;&nbsp;%d people done, used %d marks<br><span style="font-size:24px">&nbsp;&nbsp;%s</span></div></a><div class="stat"><form action="/cgi-bin/myQuestionnaire.py" method="post" id="changemk%d"><label for="user_lic">Add marks to the above questionnaire: </label><input name="addmktarget" value="%d" hidden><input id="user_lic" type="number" name="addmk" min="0" max="%d" step="1" value ="0"/></form><button type="submit" form="changemk%d" value="Submit">Submit</button></div></div><br>' % (row[0], row[7], row[9], row[3], row[5], row[0], row[0], maxmk, row[0]))



htmlTop()
get_cookie()

checkpost()

get_cookie()


body()

#get_cookie()
htmlTail()