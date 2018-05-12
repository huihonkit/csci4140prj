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
				c.execute("SELECT uname FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				nav_bar2(username[0])
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


def questionnaire():
	print('''
		<div class="category">
			<button>Art</button>
			<button>Business</button>
			<button>Education</button>
			<button>Engineering</button>
			<button>Science</button>
			<button>Social</button>			
		</div>
		<div class="content">
			questionnaire
		</div>
		''')

htmlTop()
get_cookie()
questionnaire()
htmlTail()
