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

def createDB():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	#c.execute('''CREATE TABLE user
	#		(uid integer PRIMARY KEY, uname text, password text, mark integer)''')
	#c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", ('BB55A6E76J', 'admin', 'admin', 0))
	#conn.commit()
	#c.execute('''CREATE TABLE session
	#		(sid text, uid text)''')
	#c.execute("INSERT INTO image VALUES (?, ?, ?, ?)", ('/image/a.jpg', 'public', 'BB55A6E76J', 1))
	#c.execute("INSERT INTO image VALUES (?, ?, ?, ?)", ('/image/b.png', 'private', 'BB55A6E76J', 2))
	#conn.commit()
	#c.execute('''CREATE TABLE edit
	#		(sid text, version text)''')
	c.execute('''CREATE TABLE question
		(qid integer PRIMARY KEY, uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json)''')
	conn.close()

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
		<input type = 'submit' class='qs' name='qs' value = 'create'></input>
		<button class="plus" id="plus"><h2>+</h2></button>
		</div>
		''')

#x = document.forms["myform"][""].value;
#x = document.forms["myform"][""].value;
#x = document.forms["myform"][""].value;
#createDB()
htmlTop()
nav_bar()
question()
htmlTail()