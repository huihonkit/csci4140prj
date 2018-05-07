#! /usr/bin/env python

import cgi
import cgitb
import sqlite3
import string
import random
import os
import Cookie
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

def rand_uid(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def check():
	form = cgi.FieldStorage()
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	if "username" not in form or "password" not in form or "repassword" not in form:
		msg = "<h1>Error : Please fill in all fields</h1>"
		c.execute("INSERT INTO message VALUES (?)", (msg,))
		conn.commit()
		conn.close()
		print("<meta http-equiv='refresh' content='0; url=/cgi-bin/create.py'>")
	else:
		password = form['password'].value
		repassword = form['repassword'].value
		if password != repassword:
			msg = "<h1>Error : Password does not match the confirm password</h1>"
			c.execute("INSERT INTO message VALUES (?)", (msg,))
			conn.commit()
			conn.close()
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/create.py'>")
		else:
			username = form['username'].value

			#conn = sqlite3.connect('test.db')
			#c = conn.cursor()
			uname = (username,)
			command = "SELECT password FROM user WHERE username = ?"
			c.execute(command,uname)
			result = c.fetchone()
			if result is None:
				command = "SELECT username FROM user WHERE uid = ?"
				while 1:
					uid = rand_uid()
					userid = (uid,)
					c.execute(command,userid)
					result = c.fetchone()
					if result is None:
						break
				c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (uid, username, password, 0))
				conn.commit()

				msg = "<h1>Your account has been created successfully</h1>"
				c.execute("INSERT INTO message VALUES (?)", (msg,))
				conn.commit()
				conn.close()
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
			else:
				msg = "<h1>Error : Username already exists</h1>"
				c.execute("INSERT INTO message VALUES (?)", (msg,))
				conn.commit()
				conn.close()
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/create.py'>")

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
		htmlTop()
		check()
		htmlTail()