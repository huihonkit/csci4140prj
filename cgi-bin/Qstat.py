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

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<link type="text/css" rel="stylesheet" href="/css/style.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/styleformyQ.css" />')
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")

def get_cookie():
	global myusername, myuserid
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
				myuserid = result[0]
				username = c.fetchone()
				nav_bar2(username[0])
				myusername = username[0]
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

def body():
	form = cgi.FieldStorage()
	qid = int(form.getvalue('targetQ'))
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select * from question where qid="%d"' % qid) 
	question = c.fetchone()
	uid, num_question, title, des, numdone, q = question[1], question[2], question[5], question[6], question[9], json.loads(question[8])
	print("<br><br><h1><center>Statistics for \"%s\"</center></h1><br>" % title)
	print("<span style=\"font-size:24px\"><center>%d people finished this questionnaire</center></span><br>" % numdone)
	#print("<pre class='well' style='font-size:20px'>%s</pre><br>" % des)

	print("<div class='stat'>")

	for i in range(num_question):		
		print("<span style=\"font-size:24px\">%d. %s (%s)</span><br>" % (i+1, q[i]["question"], q[i]["type"]))

		if q[i]["type"]=="mc": #print multiple question			
			for option in q[i]["answer"]:			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
				percentage = (float(howmanyofthisoption) / float(numdone)) * 100.0
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))

		elif q[i]["type"]=="shortq":
			print("<span style=\"font-size:18px\">All answers:</span><br>")
			c.execute('select answer from answer where qid="%d"' % qid)
			ans = c.fetchall()
			for row in ans:
				tempans = json.loads(row[0])
				print("<span style=\"font-size:18px\">\" %s \"</span><br>" % (tempans[i]["answer"]))

		elif q[i]["type"]=="longq":
			print("<span style=\"font-size:18px\">All answers:</span><br>")
			c.execute('select answer from answer where qid="%d"' % qid)
			ans = c.fetchall()
			for row in ans:
				tempans = json.loads(row[0])
				print("<span style=\"font-size:18px\">\"%s \"</span><br>" % (tempans[i]["answer"]))

		elif q[i]["type"]=="checkbox":
			total = 0			
			for option in q[i]["answer"]:			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						total = total + 1
					for cboption in tempans[i]["answer"]:
						if cboption == option:
							total = total + 1

			for option in q[i]["answer"]:			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
					for cboption in tempans[i]["answer"]:
						if cboption == option:
							howmanyofthisoption = howmanyofthisoption + 1
				percentage = (float(howmanyofthisoption) / float(total)) * 100.0
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))
		
		elif q[i]["type"]=="dropdown":
			for option in q[i]["answer"]:			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
				percentage = (float(howmanyofthisoption) / float(numdone)) * 100.0
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))

		elif q[i]["type"]=="ratingscale":
			minr = int(q[i]["scale"][0])
			maxr = int(q[i]["scale"][1])
			numofr = maxr - minr + 1
			#print("%d %d %d<br>" %(minr, maxr, numofr))
			for j in xrange(0, numofr):
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisrating = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if int(tempans[i]["answer"]) == (minr + j):
						howmanyofthisrating = howmanyofthisrating + 1
				percentage = (float(howmanyofthisrating) / float(numdone)) * 100.0
				print("<span style=\"font-size:18px\">%d people rated %s (%.1f%%)</span><br>" % (howmanyofthisoption, (minr + j), percentage))

		print("<br><br>")
	print("</div>")

htmlTop()
get_cookie()

body()

#get_cookie()
htmlTail()