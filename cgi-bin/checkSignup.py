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

def rand_uid(size=10, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def check():
	form = cgi.FieldStorage()
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	if "username" not in form or "password" not in form or "repassword" not in form:
		print('<script>alert("Please fill in all fields")</script>')
		print("<meta http-equiv='refresh' content='0; url=/cgi-bin/signup.py'>")
	else:
		password = form['password'].value
		repassword = form['repassword'].value
		if password != repassword:
			print('<script>alert("Password does not match the confirm password")</script>')
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/signup.py'>")
		else:
			username = form['username'].value

			#conn = sqlite3.connect('test.db')
			#c = conn.cursor()
			uname = (username,)
			command = "SELECT password FROM user WHERE uname = ?"
			c.execute(command,uname)
			result = c.fetchone()
			if result is None:
				command = "SELECT uname FROM user WHERE uid = ?"
				while 1:
					uid = int(rand_uid())
					userid = (uid,)
					c.execute(command,userid)
					result = c.fetchone()
					if result is None:
						break
				c.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", (uid, username, password, 0, 0))
				conn.commit()
				conn.close()

				print('<script>alert("Your account has been created successfully")</script>')
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
			else:
				print('<script>alert("Username already exists")</script>')
				print("<meta http-equiv='refresh' content='0; url=/cgi-bin/signup.py'>")


htmlTop()
check()
htmlTail()

