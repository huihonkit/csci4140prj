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
import sys

cgitb.enable()
def goToLogin(): 
	print'''Content-type:text/html\r\n\r\n
		<html>
		<head>
		<script>
		window.alert("You should login first before doing questionnaire!");
		</script>
		<meta http-equiv="refresh" content="0;url=login.py" />
		</head>
		<body>
		</body>
		</html>
			'''	 

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
				c.execute("SELECT uname, mark FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				htmlTop()
				nav_bar2(username[0], username[1])
			else:
				goToLogin()
			conn.close()
		except:
			goToLogin()
			sys.exit(0)

def nav_bar1():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py" style="font-family:monospace;font-size:16px;background-color:#00cc7a"><b>Quick Ques</b></a>
			
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
	print('<script src="/js/bootstrap.min.js"></script>')
	print('<link type="text/css" rel="stylesheet" href="/css/bootstrap.min.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')	
	print("</head>")
	print("<body style='background-color:#638e63'>")

def htmlTail():
	print("</body>")
	print("</html>")

def printQ():
	global qid,cuid	
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS answer(qid int, uid int, answer json, time text);')
	c.execute('select * from question where qid="%d"'%qid) 
	question=c.fetchone() #get questionaire from database
	
	print("<br><br><br>")

	#qid integer,uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json
	uid, num_question, title, des, q = question[1], question[2], question[5], question[6], json.loads(question[8])
	print("<div  class='container panel'>")
	print("<h1><center>%s</center></h1><br>"%title)
	print("<pre class='well' style='font-size:20px'>%s</pre>"%des)
	print("<br>")
	print("<form name='input' action='answer.py' method='post'>")
	print("<input name='qid' value='%d' hidden>"%qid)
	print("<input name='qNum' value='%d' hidden>"%num_question)
	print("<input name='uid' value='%d' hidden>"%cuid)
	print("<input name='startT' value='%s' hidden>"%(datetime.datetime.now().time().strftime('%H:%M:%S')))
	#start printing questions
	for i in range(num_question):		
		print("<h4><strong>%d. %s</strong></h4>"%(i+1,q[i]["question"]))
		print("<br><br>")
		if q[i]["type"]=="mc": #print multiple question			
			for option in q[i]["answer"]:
				print("<label class='radio-inline'><input type='radio' name='%d' value='%s' required>%s  </label>"%(i,option,option))
		elif q[i]["type"]=="shortq":
			print ("<input class='form-control' type='text' name='%d' required/>" %i)
		elif q[i]["type"]=="longq":
			print ("<textarea class='form-control' rows='6' cols='100' name='%d' required> </textarea>" %i)
		elif q[i]["type"]=="checkbox":
			for option in q[i]["answer"]:
				print ("<label class='checkbox-inline'><input type='checkbox' name='%d' value='%s' >%s  </label>" %(i,option,option))
		elif q[i]["type"]=="dropdown":
			print ("<select class='input2' name='%d'>"%i)
			for option in q[i]["answer"]:				
				print ("<option value='%s'>%s</option>" %(option,option))
			print ("</select>")
		elif q[i]["type"]=="ratingscale":
			mid=0;
			if ((int(q[i]["scale"][0])+int(q[i]["scale"][1]))%2==0):
				mid=(int(q[i]["scale"][0])+int(q[i]["scale"][1]))/2
			else:
				mid=(int(q[i]["scale"][0])+int(q[i]["scale"][1]))/2+1
			print ('<div style="width:400px"><span>%s</span><span style="float:right">%s</span><input style="width:400px" name="%d" type="range" min="%d" max="%d" value="%d" id="%d"></input></div>' %(q[i]["label"][0],q[i]["label"][1],i,int(q[i]["scale"][0]),int(q[i]["scale"][1]),mid,i))
			print ("<p>Value: <span id='%dvalue'></span></p>"%(i))
			print('''<script>var slider%d = document.getElementById("%d");
					var output%d = document.getElementById("%dvalue");
					output%d.innerHTML = slider%d.value; 					
					slider%d.oninput = function() {
					    output%d.innerHTML = this.value;
					}</script>'''%(i,i,i,i,i,i,i,i))
		print ("<br><br><br>")
	print("<center><input class='btn btn-success' type='submit' value='Submit'></center>")
	print("<br><br>")
	print("</form>")
	print("</div>")
	conn.close()

if __name__ == "__main__":	
	cuid=-1		
	form=cgi.FieldStorage()
	qid = int(form.getvalue('qid'))
	#qid=4 #*******************************need to delete after index page finished**********************************
	get_cookie()
	
	printQ()
	htmlTail()
	
