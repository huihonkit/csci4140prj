#! /usr/bin/env python

import cgi
import cgitb
import os
import Cookie
import sqlite3
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

def create_form():
	print("<form action = '/cgi-bin/checkCreate.py' method = 'post'>")
	print("<h3>username</h3>")
	print("<input type = 'text' name = 'username'></input>")
	print("<h3>password</h3>")
	print("<input type = 'text' name = 'password'></input>")
	print("<h3>retype password</h3>")
	print("<input type = 'text' name = 'repassword'></input>")
	print("<input type = 'submit' name = 's1' value = 'create'></input>")
	print("</form>")

def back():
	print("<form action = '/cgi-bin/index.py' method = 'post'>")
	print("<input type = 'submit' name = 'back' value = 'back to index'></input>")
	print("</form>")

def message():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("SELECT mess FROM message")
	result = c.fetchone()
	if result is not None:
		print(result[0])
		c.execute("DELETE FROM message")
		conn.commit()
	conn.close()

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
		message()
		create_form()
		back()
		htmlTail()