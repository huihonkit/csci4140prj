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
import json
cgitb.enable()

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<link type="text/css" rel="stylesheet" href="/css/style.css" />')
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
			conn.close()
			test(result[0])
		except:
			print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")

def test(uid):
	data = cgi.FieldStorage()
	d = data['data'].value
	obj = json.loads(d)
	title = obj["title"]
	des = obj["description"]
	question = obj["question"]
	myjson = json.dumps(question)
	time = obj["time"]
	category = obj["category"]
	mark = obj["mark"]
	num = obj["num"]
	total = obj["total"]
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("INSERT INTO question(uid, num_question, use_mark, time, title, des, category, question, num_done) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (uid, num, mark, time, title, des, category, myjson, 0))
	conn.commit()
	c.execute("SELECT mark FROM user WHERE uid = ?", (uid,))
	result = c.fetchone()
	total = result[0] - total
	c.execute("UPDATE user SET mark=? WHERE uid = ?", (total, uid))
	conn.commit()
	conn.close()
	print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")

htmlTop()
get_cookie()
htmlTail()