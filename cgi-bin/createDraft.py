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
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')
	print('<script src="/js/createQuestion.js"></script>')
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
		#try:
		data = c['csci414064769'].value
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		c.execute("SELECT uid FROM session WHERE sid = ?", (data,))
		result = c.fetchone()
		conn.close()
		content(result[0])
		#except:
		#	print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")


def content(uid):
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
	c.execute("INSERT INTO draft(uid, num_question, use_mark, time, title, des, category, question) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (uid, num, mark, time, title, des, category, myjson))
	conn.commit()
	conn.close()
	print("<meta http-equiv='refresh' content='0; url=/cgi-bin/index.py'>")

htmlTop()
get_cookie()
htmlTail()