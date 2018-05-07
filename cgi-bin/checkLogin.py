#! /usr/bin/env python

import cgi
import cgitb
import sqlite3
import string
import random
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

def rand_sid(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def check(sid):
	form = cgi.FieldStorage()
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	if "username" not in form or "password" not in form:
		msg = "<h1>Error : Please fill in the username and password fields</h1>"
		c.execute("INSERT INTO message VALUES (?)", (msg,))
		conn.commit()
		conn.close()
		print("<meta http-equiv='refresh' content='0; url=/cgi-bin/login.py'>")
	else:
		username = form['username'].value
		password = form['password'].value

		uname = (username,)
		command = "SELECT password, uid FROM user WHERE username = ?"
		c.execute(command,uname)
		result = c.fetchone()
		if result is None:
			msg = "<h1>Error : You have entered an invalid username or password</h1>"
			c.execute("INSERT INTO message VALUES (?)", (msg,))
			conn.commit()
			conn.close()
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/login.py'>")
		else:
			if(result[0] == password):
				c.execute("INSERT INTO session VALUES (?, ?)", (sid,result[1]))
				msg = "<h1>You have successfully logged in</h1>"
				c.execute("INSERT INTO message VALUES (?)", (msg,))
				conn.commit()
				conn.close()
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
			else:
				msg = "<h1>Error : You have entered an invalid username or password</h1>"
				c.execute("INSERT INTO message VALUES (?)", (msg,))
				conn.commit()
				conn.close()
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/login.py'>")

def set_cookie():
	ck = Cookie.SimpleCookie()
	command = "SELECT uid FROM session WHERE sid = ?"
	while 1:
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		sid = rand_sid()
		seid = (sid,)
		c.execute(command,seid)
		result1 = c.fetchone()
		if result1 is None:
			break
	ck['csci414064769'] = sid
	ck['csci414064769']['expires'] = 60 * 60
	print(ck)
	return sid

if 'HTTP_COOKIE' in os.environ:
	cookie_string = os.environ.get('HTTP_COOKIE')
	ck = Cookie.SimpleCookie()
	ck.load(cookie_string)
	try:
		data = ck['csci414064769'].value
		htmlTop()
		print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
		htmlTail()
	except:
		sid = set_cookie()
		htmlTop()
		check(sid)
		htmlTail()