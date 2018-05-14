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
import ast
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
			<a href="index.py" style="font-family:monospace;font-size:16px;background-color:#00cc7a"><b>Quick Ques</b></a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
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
		<input type='submit' class='qs' name='qs' value = 'Create'></input>
		<input type='submit' class='qs' name='draft' value='Draft'></input>
		<button class="plus" id="plus"><h2>Add more question</h2></button>
		</div>
		''')

def draft():
	data = cgi.FieldStorage()
	if data.has_key("did"):
		did = data["did"].value
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		c.execute("SELECT * FROM draft WHERE did = ?", (did,))
		result = c.fetchone()
		title = "<script>document.getElementsByName('title')[0].value = '" + str(result[5]) + "';</script>"
		print(title)
		des = "<script>document.getElementsByName('des')[0].value = '" + str(result[6]) + "';</script>"
		print(des)
		print('<script src="/js/draft.js"></script>')
		num_question = result[2] - 1;
		while num_question > 0:
			print("<script>addquestion()</script>")
			num_question = num_question - 1
		print("<script>prepare('"+str(result[2])+"','"+result[8]+"')</script>")
		print("<script>settime('"+result[4]+"')</script>")
		print("<script>var c = document.getElementsByName('category')[0];</script>")
		if(result[7] == "art"):
			print("<script>c.selectedIndex = 0;</script>")
		elif(result[7] == "business"):
			print("<script>c.selectedIndex = 1;</script>")
		elif(result[7] == "education"):
			print("<script>c.selectedIndex = 2;</script>")
		elif(result[7] == "engineering"):
			print("<script>c.selectedIndex = 3;</script>")
		elif(result[7] == "science"):
			print("<script>c.selectedIndex = 4;</script>")
		else:
			print("<script>c.selectedIndex = 5;</script>")
		print("<script>document.getElementsByName('mark')[0].value = " + str(result[3]) + ";</script>")
		c.execute("DELETE FROM draft WHERE did = ?", (did,))
		conn.commit()
		conn.close()

htmlTop()
get_cookie()
question()
draft()
htmlTail()