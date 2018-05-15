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
from sklearn.externals import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

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
	startT = form.getvalue('startT')
	#currentT=datetime.datetime.now().replace(microsecond=0)
	currentT=datetime.datetime.now().time().strftime('%H:%M:%S')
	t = datetime.datetime.strptime(currentT,'%H:%M:%S')-datetime.datetime.strptime(startT,"%H:%M:%S")

	data=[]
	for i in range(int(qNum)):
		ans=form.getvalue('%d'%i)
		data.append({'answer':ans})	#save each question's answer

	data = json.dumps(data)
	conn = sqlite3.connect('test.db')
	c = conn.cursor()

	c.execute("SELECT * from question where qid='%d'"%(int(qid)))
	questionnaire=c.fetchone()
	num_done=int(questionnaire[9])
	num_done+=1
	numQ=int(questionnaire[2])
	marks=numQ
	c.execute("SELECT mark from user where uid='%d'"%(int(uid)))
	userMarks=c.fetchone()
	marks+=int(userMarks[0])	
	
	c.execute("UPDATE user SET mark = %d WHERE uid='%d'"%(marks,int(uid)))#increase user's marks
	conn.commit()
	c.execute("insert into answer values('%d','%d','%s','%s')"%(int(qid),int(uid),data,t))
	conn.commit()
	c.execute("UPDATE question SET num_done = %d WHERE qid = %d"%(num_done,int(qid)))#increase num_done
	conn.commit()

	second = t.total_seconds()
	c.execute("SELECT est from question where qid='%d'"%(int(qid)))
	est = c.fetchone()[0]
	est = int(round(((second - est)/est) *100))
	print(est)
	c.execute("SELECT credit from user where uid='%d'"%(int(uid)))
	credit = c.fetchone()[0]
	feature = np.array([[est,credit]])
	model = joblib.load('save/model.pkl')
	predict = model.predict(feature)
	credit = credit + 1
	c.execute("UPDATE user SET credit = %d WHERE uid='%d'"%(credit,int(uid)))
	conn.commit()
	c.execute("INSERT INTO predict(qid, uid, predict) VALUES (?, ?, ?)", (int(qid), int(uid), int(predict[0])))
	conn.commit()
	
	conn.close()

if __name__ == "__main__":
	saveAnswer()
	html()

	
	