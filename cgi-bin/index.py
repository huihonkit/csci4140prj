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
	print('<script src="/js/bootstrap.min.js"></script>')
	print('<link type="text/css" rel="stylesheet" href="/css/bootstrap.min.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')
	print('<script src="/js/category.js"></script>')
	print('''<style>
		.hv{border-style: dashed;border-radius:15px;background-color:#F0FFF0;border-color:#2F4F4F}
		.hv:hover{
			border-style:solid;
		}
		</style>''')
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
				nav_bar2(username[0], username[1])
				
				DB(result[0])
				conn.close()
				#DB(result[0])
			else:
				nav_bar1()
				conn.close()
				DB2()
		except:
			nav_bar1()
			DB2()
			


def DB(uid):
	
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	
	c.execute("SELECT qid FROM answer WHERE uid = ?", (uid,))
	results = c.fetchall()
	if results is not None:
	#qid = result[0]
		qid = []
		for result in results:
			qid.append(result[0])
		#rownum = c.execute("SELECT * FROM question WHERE uid != '%s' and qid not IN (%s) ORDER BY use_mark DESC"%(uid, ",".join('?'*qid),qid))

	

	rownum = c.execute("SELECT * FROM question WHERE uid != ? ORDER BY use_mark DESC", (uid, ))
		
	for i in rownum:

	#print(i)
		if (i[0] not in qid):
			mystr = "onclick='myfun("+str(i[0])+")'"
			
			print("<div class='"+i[7]+" container hv' "+mystr+">"+"<p style='font-size:24px'><b>%s</b>&nbsp<i style='font-size:17px'>%s</i></p><p style='font-size:21px'>%s</p></div>"%(str(i[5]),str(i[7]),str(i[6])))
			print('<br>')
		
	conn.close()

				

def DB2():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	rownum = c.execute("SELECT * FROM question ORDER BY use_mark DESC")
					
	for i in rownum:
		#print(i)
		mystr = "onclick='myfun("+str(i[0])+")'"
		print("<div class='"+i[7]+" container hv' "+mystr+">"+"<p style='font-size:24px'><b>%s</b>&nbsp<i style='font-size:17px'>%s</i></p><p style='font-size:21px'>%s</p></div>"%(str(i[5]),str(i[7]),str(i[6])))
		print('<br>')

	conn.close()
				
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

def questionnaire():
	print('''<center>
		<div class="category">
			<button class='btn btn-success btn-lg' id="All">All</button>
			<button class='btn btn-success btn-lg' id="Art">Art</button>
			<button class='btn btn-success btn-lg' id="Business">Business</button>
			<button class='btn btn-success btn-lg' id="Education">Education</button>
			<button class='btn btn-success btn-lg' id="Engineering">Engineering</button>
			<button class='btn btn-success btn-lg' id="Science">Science</button>
			<button class='btn btn-success btn-lg' id="Social">Social</button>			
		</div>
		</center>
		<br>
		''')


htmlTop()
questionnaire()
get_cookie()
#questionnaire()
htmlTail()
