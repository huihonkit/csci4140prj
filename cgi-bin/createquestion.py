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
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')
	print('<script src="/js/createQuestion.js"></script>')
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
				c.execute("SELECT uname, mark FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				nav_bar(username[0],username[1])
			else:
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
			conn.close()
		except:
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")

def nav_bar(uname, mark):
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
	print("<a>Mark:"+str(mark)+"</a>")
	print('''
			<a href="logout.py">Logout</a>
		</div>
		''')
	print('</div>')

def question():
	print('''
		<div class="content">
		<h4>Title</h4>
		<input class="input1" type = 'text' name = 'title'></input>
		<h4>Description(optional)</h4>
		<textarea class="input1" name="des" rows="4" cols="50"></textarea>
		<br>
		<hr id="hr">
		<h4>Closed Time</h4>
		<input class="input2" type = 'date' name = 'time'></input>
		<br>
		<h4>Category</h4>
		<select class="input2" name="category">
		<option value="art">Art</option>
		<option value="business">Business</option>
		<option value="education">Education</option>
		<option value="engineering">Engineering</option>
		<option value="science">Science</option>
		<option value="social">Social</option>
		</select>
		<br>
		<h4>Extra Mark<button disabled title="Higher mark = Higher priority">?</button></h4>
		<input class="input3" type = 'number' name = 'mark' value=0 min="0"></input>
		<br>
		<h4 id="total">Total Mark: <button disabled title="Total mark = 3*number of question + extra mark">?</button></h4>
		<input type = 'submit' class='qs' name='qs' value = 'create'></input>
		<button class="plus" id="plus"><h2>Add more question</h2></button>
		</div>
		''')

htmlTop()
get_cookie()
question()
htmlTail()