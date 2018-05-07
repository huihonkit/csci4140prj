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

def signup():
	print('''
		<div class="signup">
		<h1>Create a New Account</h1>
		<form action="/cgi-bin/checksignup.py method="post">
		<br>
		<input class="input1" type="text" placeholder="Username" name="username" required>
		<br>
		<input class="input1" type="text" placeholder="Password" name="password" required>
		<br>
		<input class="input2" type ="submit" value ="Sign up"></input>
		</form>
		</div>
		''')


htmlTop()
signup()
htmlTail()