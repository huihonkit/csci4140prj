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
import datetime
import json

cgitb.enable()

def get_cookie():
	global cuid
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
			cuid=result[0]
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

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')	
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
		<h4>Mark<button disabled title="Higher mark = Higher priority">?</button></h4>
		<input class="input3" type = 'number' name = 'mark'></input>
		<br>
		<input type = 'submit' class='qs' name='qs' value = 'create'></input>
		<button class="plus" id="plus"><h2>+</h2></button>
		</div>
		''')

def printQ():
	global qid,cuid
	get_cookie()
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS answer(qid int, uid int, answer json, time text);')
	c.execute('select * from question where qid="1"') #get qid from index page. ***need change***
	question=c.fetchone() #get questionaire from database
	
	print("<br><br><br>")

	#qid integer,uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json
	uid, num_question, title, des, q=question[1], question[2], question[5], question[6], json.loads(question[8])
	
	print("<h1>%s</h1>"%title)
	print(des)
	print("<br><br>")
	print("<form name='input' action='answer.py' method='post'>")
	print("<input name='qid' value='%d' hidden>"%qid)
	print("<input name='qNum' value='%d' hidden>"%num_question)
	print("<input name='uid' value='%d' hidden>"%cuid)
	for i in range(num_question):
		print ("%d. "%(i+1))
		print(q[i]["question"])
		print("<br>")
		if q[i]["type"]=="multiple": #print multiple question			
			for option in q[i]["answer"]:
				print("<input type='radio' name='%d' value='%s' required>%s  "%(i,option,option))
		elif q[i]["type"]=="shortQuestion":
			print ("<input type='text' name='%d' required/>" %i)
		print ("<br><br>")
	print("<input type='submit' value='Submit'>")
	print("</form>")
	conn.close()

if __name__ == "__main__":
	qid=-1
	cuid=-1
	htmlTop()	
	printQ()
	htmlTail()
	