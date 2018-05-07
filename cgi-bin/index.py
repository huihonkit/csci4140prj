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
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")
'''
def login():
	print("<form action = '/cgi-bin/login.py' method = 'post'>")
	print("<input type = 'submit' name = 's1' value = 'login'></input>")
	print("</form>")

def create():
	print("<form action = '/cgi-bin/create.py' method = 'post'>")
	print("<input type = 'submit' name = 's2' value = 'create'></input>")
	print("</form>")

def get_uid():
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
			return result[0]
		except:
			return ''

def show_image():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("SELECT * FROM image ORDER BY ct DESC")
	result = c.fetchall()
	if result is not None:
		path = []
		uid = get_uid()
		for data in result:
			if data[1] == 'public':
				ipath = ".." + data[0]
				path.append(ipath)
			else:
				if uid == data[2]:
					ipath = ".." + data[0]
					path.append(ipath)
		conn.close()
		if len(path) != 0:
			page = 1
			form = cgi.FieldStorage()
			if "page" in form:
				page = int(form['page'].value)
			print("<h3>Current page:" + str(page) +"</h3>")
			first = (page - 1) * 8
			while first < len(path):
				imgpath = path[first]
				print("<div id='idiv'>")
				print("<img src=" + imgpath + " id='simg'>")
				print("</div>")
				print("<a href = " + imgpath + ">permalink</a>")
				print("<br>")
				first = first + 1
				if first == page * 8:
					break
			max_page = math.ceil(float(len(path)) / 8)
			if(max_page == 0):
				max_page = 1
			cur_page = 1
			while cur_page <= max_page:
				print("<form action = '/cgi-bin/index.py' method = 'get'>")
				print("<input type = 'submit' name = 'page' value = " + str(cur_page) + "></input>")
				print("</form>")
				cur_page = cur_page + 1
		else:
			print("<h3>no photo</h3>")

def upload():
	print("<h3>Upload photo</h3>")
	print("<form action = '/cgi-bin/upload.py' method = 'post' enctype='multipart/form-data'>")
	print("<input type = 'file' name = 'filename'></input>")
	print("<input type = 'radio' name = 'visibility' value = 'public' checked>public</input>")
	print("<input type = 'radio' name = 'visibility' value = 'private'>private</input>")
	print("<input type = 'submit' name = 'upload' value = 'upload'>")
	print("</form>")

def error_msg():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("SELECT mess FROM message")
	result = c.fetchone()
	if result is not None:
		print(result[0])
		c.execute("DELETE FROM message")
		conn.commit()
	conn.close()

def logout():
	print("<form action = '/cgi-bin/logout.py' method = 'post'>")
	print("<input type = 'submit' name = 's3' value = 'logout'></input>")
	print("</form>")

def update():
	print("<form action = '/cgi-bin/update.py' method = 'post'>")
	print("<input type = 'submit' name = 's4' value = 'update'></input>")
	print("</form>")

def get_cookie():
	if 'HTTP_COOKIE' in os.environ:
		cookie_string = os.environ.get('HTTP_COOKIE')
		c = Cookie.SimpleCookie()
		c.load(cookie_string)
		try:
			data = c['csci414064769'].value
			error_msg()
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			c.execute("SELECT uid FROM session WHERE sid = ?", (data,))
			result = c.fetchone()
			c.execute("SELECT username FROM user WHERE uid = ?", (result[0],))
			username = c.fetchone()
			conn.close()
			print("<h3>username:" + username[0] + "</h3>")
			update()
			show_image()
			upload()
			logout()
		except:
			error_msg()
			login()
			create()
			show_image()
			upload()
'''
def nav_bar():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
			<a href="createquestion.py">Create Questionnaire</a>
		</div>
		<div class="right">
			<a href="signin.py">Sign in</a>
			<a href="signup.py">Sign up</a>
		</div>
		''')
	print('</div>')

def questionnaire():
	print('''
		<div class="content">
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		questionnaire
		</div>
		''')

htmlTop()
nav_bar()
questionnaire()
#get_cookie()
htmlTail()