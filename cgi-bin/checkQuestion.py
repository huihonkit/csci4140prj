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
import json
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

def test():
	data = cgi.FieldStorage()
	#print(data)
	d = data['data'].value
	obj = json.loads(d)
	title = obj["title"]
	des = obj["description"]
	question = obj["question"]
	myjson = json.dumps(question)
	time = obj["time"]
	category = obj["category"]
	mark = obj["mark"]
	num = obj["num"]
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("INSERT INTO question VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (1, 1, num, mark, time, title, des, category, myjson))
	conn.commit()
	conn.close()

htmlTop()
#nav_bar()
test()
htmlTail()