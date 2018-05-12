#! /usr/bin/env python

import cgi
import cgitb
import sqlite3
import Cookie
import os
cgitb.enable()

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>assignment1</title>")
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")

def login_form():
	print("<form action = '/cgi-bin/checkLogin.py' method = 'post'>")
	print("<h3>username</h3>")
	print("<input type = 'text' name = 'username'></input>")
	print("<h3>password</h3>")
	print("<input type = 'text' name = 'password'></input>")
	print("<input type = 'submit' name = 's1' value = 'login'></input>")
	print("</form>")

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
login_form()
back()
htmlTail()
