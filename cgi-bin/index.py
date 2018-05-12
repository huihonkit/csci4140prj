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
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")



def login():
	print("<form action = '/cgi-bin/login.py' method = 'post'>")
	print("<input type = 'submit' name = 's1' value = 'login'></input>")
	print("</form>")



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


def logout():
	print("<form action = '/cgi-bin/logout.py' method = 'post'>")
	print("<input type = 'submit' name = 's3' value = 'logout'></input>")
	print("</form>")


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
				print(result)
				c.execute("SELECT uname FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				nav_bar2(username[0])
			else:
				nav_bar1()
			conn.close()
			#print("<h3>username:" + username[0] + "</h3>")
			#update()
			#show_image()
			#upload()
			#logout()
		except:
			nav_bar1()



def nav_bar1():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="#home">Home</a>
			<a href="#myQuestionnaire">MyQuestionnaire</a>
			<a href="#search">Search</a>
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
			<a href="#home">Home</a>
			<a href="#myQuestionnaire">MyQuestionnaire</a>
			<a href="#search">Search</a>
		</div>
		<div class="right">''')
	print("<a>"+uname+"</a>")
	print('''
			<a href="logout.py">Logout</a>
		</div>
		''')
	print('</div>')


def questionnaire():
	print('''
		<div class="content">
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		</div>
		''')

htmlTop()
#nav_bar()
#questionnaire()
get_cookie()
questionnaire()
htmlTail()