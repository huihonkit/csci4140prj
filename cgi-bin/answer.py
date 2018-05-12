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
import datetime
import json

cgitb.enable()

#redirect to index page
def html(): 
	print'''Content-type:text/html\r\n\r\n
		<html>
		<head>
		<meta http-equiv="refresh" content="0;url=index.py" />
		</head>
		<body>
		</body>
		</html>
			'''

def saveAnswer():
	form=cgi.FieldStorage()
	qid = form.getvalue('qid')
	uid = form.getvalue('uid')
	qNum = form.getvalue('qNum')
	data=[]
	for i in range(int(qNum)):
		ans=form.getvalue('%d'%i)
		data.append({'answer':ans})	#save each question's answer

	data = json.dumps(data)

	currentT=datetime.datetime.now() #get current time
	t = currentT.strftime("%d-%b-%Y %H:%M:%S")	

	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute("SELECT num_done from question where qid=%d"%(int(qid)))
	num_done=c.fetchone()
	num_done=int(num_done[0])
	num_done+=1
	c.execute("insert into answer values('%d','%d','%s','%s')"%(int(qid),int(uid),data,t))
	conn.commit()
	c.execute("UPDATE question SET num_done = %d WHERE qid = %d"%(num_done,int(qid)))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	saveAnswer()
	html()

	
	