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
	print('<script src="/js/jquery-3.3.1.min.js"></script>')
	print('<script src="/js/category.js"></script>')
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


def nav_bar2(uname, mark):
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
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
	print('''
		<div class="category">
			<button id="All">All</button>
			<button id="Art">Art</button>
			<button id="Business">Business</button>
			<button id="Education">Education</button>
			<button id="Engineering">Engineering</button>
			<button id="Science">Science</button>
			<button id="Social">Social</button>			
		</div>
		<div class="content">
			username	title	description		category
			<br>
			<br>
			<hr>
		</div>
		''')

def DB():
		
	conn = sqlite3.connect('test.db')
	c1 = conn.cursor()

	if 'HTTP_COOKIE' in os.environ:
			cookie_string = os.environ.get('HTTP_COOKIE')
			c = Cookie.SimpleCookie()
			c.load(cookie_string)
			try:
				data = c['csci414064769'].value
				c1.execute("SELECT uid FROM session WHERE sid = ?", (data,))
				result = c1.fetchone()
				if result is not None:
					rownum = c1.execute("SELECT * FROM question WHERE uid != ?", (result[0],))
				else:
					rownum = c1.execute("SELECT * FROM question")

				
				for i in rownum:
					#print(i)
					mystr = "onclick='myfun("+str(i[0])+")'"
					if i[7] == "art":
						print("<div class='art' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "business":
						print("<div class='business' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "education":
						print("<div class='education' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "engineering":
						print("<div class='engineering' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "science":
						print("<div class='science' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					else:
						print("<div class='social' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")	
					print("<hr>")
					conn.close()

			except:
				

				rownum = c1.execute("SELECT * FROM question")

				for i in rownum:
					#print(i)
					mystr = "onclick='myfun("+str(i[0])+")'"
					if i[7] == "art":
						print("<div class='art' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "business":
						print("<div class='business' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "education":
						print("<div class='education' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "engineering":
						print("<div class='engineering' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					elif i[7] == "science":
						print("<div class='science' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")
					else:
						print("<div class='social' "+mystr+">"+str(i[5])+str(i[6])+str(i[7])+"</div>")	
					print("<hr>")
				conn.close()




htmlTop()
get_cookie()
questionnaire()
DB()
htmlTail()
