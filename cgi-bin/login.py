#! /usr/bin/env python

import cgi
import cgitb
import sqlite3
import Cookie
import os
cgitb.enable()
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
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")

def login_form():
	print("<br><br><center><div class='signup'>")
	print("<form action = '/cgi-bin/checkLogin.py' method = 'post'>")
	print("<h3>Login</h3>")
	print("<input type = 'text' class='input1' placeholder='Username' style='width:300px' name = 'username'></input><br>")	
	print("<input type = 'text' class='input1' placeholder='Password' style='width:300px' name = 'password'></input><br><br>")
	print("<input type = 'submit' class='input2' name = 's1' value = 'login'></input>")
	print("</form>")
	print("</div></center>")

def back():
	print("<form action = '/cgi-bin/index.py' method = 'post'>")
	print("<input type = 'submit' name = 'back' value = 'back to index'></input>")
	print("</form>")

def start():
	if 'HTTP_COOKIE' in os.environ:
		cookie_string = os.environ.get('HTTP_COOKIE')
		ck = Cookie.SimpleCookie()
		ck.load(cookie_string)
		try:
			data = ck['csci414064769'].value
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			sid = (data,)
			command = "SELECT uid FROM session WHERE sid = ?"
			c.execute(command,sid)
			result = c.fetchone()
			conn.close()
			if result is not None:
				htmlTop()
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
				htmlTail()
			else:
				conn = sqlite3.connect('test.db')
				c = conn.cursor()
				c.execute("SELECT message FROM message")
				result = c.fetchone()
				if result is not None:
					ck = Cookie.SimpleCookie()
					ck['csci414064769'] = ''
					ck['csci414064769']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
					print(ck)
					htmlTop()
					print(result[0])
					c.execute("DELETE FROM message")
					conn.commit()
					conn.close()
					login_form()
					back()
					htmlTail()
				else:
					conn.close()
					htmlTop()
					login_form()
					back()
					htmlTail
		except:
			htmlTop()
			login_form()
			back()
			htmlTail()

#start()
htmlTop()
get_cookie()
login_form()
htmlTail()
