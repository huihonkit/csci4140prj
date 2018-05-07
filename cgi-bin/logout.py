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

def delete_session():
	if 'HTTP_COOKIE' in os.environ:
		cookie_string = os.environ.get('HTTP_COOKIE')
		ck = Cookie.SimpleCookie()
		ck.load(cookie_string)
		try:
			data = ck['csci414064769'].value
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			sid = (data,)
			command = "DELETE FROM session WHERE sid = ?"
			c.execute(command,sid)
			conn.commit()
			conn.close()
		except:
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")

delete_session()
ck = Cookie.SimpleCookie()
ck['csci414064769'] = ''
ck['csci414064769']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
print(ck)
htmlTop()
print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")
htmlTail()