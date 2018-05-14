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
def get_cookie():
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
				c.execute("SELECT uname, mark FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
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
			<a href="index.py" style="font-family:monospace;font-size:16px;background-color:#00cc7a"><b>Quick Ques</b></a>
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
			<a href="index.py" style="font-family:monospace;font-size:14px;background-color:#00cc7a"><b>Quick Ques</b></a>
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

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<link type="text/css" rel="stylesheet" href="/css/style.css" />')	
	print('<script src="/js/bootstrap.min.js"></script>')
	print('<link type="text/css" rel="stylesheet" href="/css/bootstrap.min.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')	
	print('<script src="/js/category.js"></script>')
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")

def signup():
	print('''
		<div class="signup">
		<h1>Create a New Account</h1>
		<form action="/cgi-bin/checkSignup.py" method="post">
		<br>
		<input class="input1" type="text" placeholder="Username" name="username" required>
		<br>
		<input class="input1" type="text" placeholder="Password" name="password" required>
		<br>
		<input class="input1" type="text" placeholder="Retype password" name="repassword" required>
		<br>
		<input class="input2" type ="submit" value ="Sign up"></input>
		</form>
		</div>
		''')


htmlTop()
get_cookie()
signup()
htmlTail()
