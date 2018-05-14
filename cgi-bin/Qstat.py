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
import sys
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
#from pylab import figure, axes, pie, title, show
cgitb.enable()

def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print("<script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>")
	print('<link type="text/css" rel="stylesheet" href="/css/style.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/styleformyQ.css" />')
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
			if result is not None:
				c.execute("SELECT uname, mark FROM user WHERE uid = ?", (result[0],))
				username = c.fetchone()
				nav_bar2(username[0], username[1])
			else:
				nav_bar1()
			conn.close()
		except:
			nav_bar1()

def nav_bar1():
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="search.py">Search</a>
		</div>
		<div class="right">
			<a href="login.py">Sign in</a>
			<a href="signup.py">Sign up</a>
		</div>
		''')
	print('</div>')


def nav_bar2(uname, mark):
	print('<div class="navbar">')
	print('''
		<div class="left">
			<a href="index.py">Home</a>
			<a href="myQuestionnaire.py">My Questionnaire</a>
			<a href="search.py">Search</a>
			<a href="createquestion.py">Create Questionnaire</a>
			<a href="myDraft.py">My Draft</a>
		</div>
		<div class="right">''')
	print("<a>"+uname+"</a>")
	print("<a>Mark:"+str(mark)+"</a>")
	print('''
			<a href="logout.py">Logout</a>
		</div>
		''')
	print('</div>')

def body():
	form = cgi.FieldStorage()
	qid = int(form.getvalue('targetQ'))
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	c.execute('select * from question where qid="%d"' % qid) 
	question = c.fetchone()
	uid, num_question, title, des, numdone, q = question[1], question[2], question[5], question[6], question[9], json.loads(question[8])
	print("<br><br><h1><center>Statistics for \"%s\"</center></h1><br>" % title)
	print("<span style=\"font-size:24px\"><center>%d people finished this questionnaire</center></span><br>" % numdone)
	#print("<pre class='well' style='font-size:20px'>%s</pre><br>" % des)

	print("<div class='stat'>")

	for i in range(num_question):		
		print("<span style=\"font-size:24px\">%d. %s (%s)</span><br>" % (i+1, q[i]["question"], q[i]["type"]))

		if q[i]["type"]=="mc": #print multiple question	
			outerl = [['Option', 'Number']]
			for option in q[i]["answer"]:
				innerl = []
				#print option.encode("ascii")
				innerl.append(option.encode("ascii"))			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
				if numdone == 0 or howmanyofthisoption == 0:
					tempstat = 0
				else: 
					tempstat = (float(howmanyofthisoption) / float(numdone))
				percentage = float(tempstat) * 100.0
				innerl.append(howmanyofthisoption)
				outerl.append(innerl)
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))

			print('''
				<div id="piechart%d"></div>
				<script type="text/javascript">
				google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawChart);

				function drawChart() {
					var data = google.visualization.arrayToDataTable(%s);

 				// Optional; add a title and set the width and height of the chart
 				var options = {'width':550, 'height':400};

				// Display the chart inside the <div> element with id="piechart"
				var chart = new google.visualization.PieChart(document.getElementById('piechart%d'));
				chart.draw(data, options);
				}
				</script>
				''' % (i, outerl, i))

		elif q[i]["type"]=="shortq":
			print("<span style=\"font-size:18px\">All answers:</span><br>")
			c.execute('select answer from answer where qid="%d"' % qid)
			ans = c.fetchall()
			for row in ans:
				tempans = json.loads(row[0])
				print("<span style=\"font-size:18px\">\" %s \"</span><br>" % (tempans[i]["answer"]))

		elif q[i]["type"]=="longq":
			print("<span style=\"font-size:18px\">All answers:</span><br>")
			c.execute('select answer from answer where qid="%d"' % qid)
			ans = c.fetchall()
			for row in ans:
				tempans = json.loads(row[0])
				print("<span style=\"font-size:18px\">\"%s \"</span><br>" % (tempans[i]["answer"]))

		elif q[i]["type"]=="checkbox":
			total = 0
			outerl = [['Option', 'Number']]
			for option in q[i]["answer"]:			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						total = total + 1
					for cboption in tempans[i]["answer"]:
						if cboption == option:
							total = total + 1

			for option in q[i]["answer"]:
				innerl = []
				#print option.encode("ascii")
				innerl.append(option.encode("ascii"))		
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
					for cboption in tempans[i]["answer"]:
						if cboption == option:
							howmanyofthisoption = howmanyofthisoption + 1
				if numdone == 0 or howmanyofthisoption == 0 or total == 0:
					tempstat = 0
				else: 
					tempstat = (float(howmanyofthisoption) / float(total))
				percentage = float(tempstat) * 100.0
				innerl.append(howmanyofthisoption)
				outerl.append(innerl)
				#percentage = (float(howmanyofthisoption) / float(total)) * 100.0
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))
			print('''
				<div id="piechart%d"></div>
				<script type="text/javascript">
				google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawChart);

				function drawChart() {
					var data = google.visualization.arrayToDataTable(%s);

 				// Optional; add a title and set the width and height of the chart
 				var options = {'width':550, 'height':400};

				// Display the chart inside the <div> element with id="piechart"
				var chart = new google.visualization.PieChart(document.getElementById('piechart%d'));
				chart.draw(data, options);
				}
				</script>
				''' % (i, outerl, i))

		elif q[i]["type"]=="dropdown":
			outerl = [['Option', 'Number']]
			for option in q[i]["answer"]:
				innerl = []
				#print option.encode("ascii")
				innerl.append(option.encode("ascii"))			
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisoption = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if tempans[i]["answer"] == option:
						howmanyofthisoption = howmanyofthisoption + 1
				if numdone == 0 or howmanyofthisoption == 0:
					tempstat = 0
				else: 
					tempstat = (float(howmanyofthisoption) / float(numdone))
				percentage = float(tempstat) * 100.0
				innerl.append(howmanyofthisoption)
				outerl.append(innerl)
				print("<span style=\"font-size:18px\">%d people chose option \"%s\" (%.1f%%)</span><br>" % (howmanyofthisoption, option, percentage))
			print('''
				<div id="piechart%d"></div>
				<script type="text/javascript">
				google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawChart);

				function drawChart() {
					var data = google.visualization.arrayToDataTable(%s);

 				// Optional; add a title and set the width and height of the chart
 				var options = {'width':550, 'height':400};

				// Display the chart inside the <div> element with id="piechart"
				var chart = new google.visualization.PieChart(document.getElementById('piechart%d'));
				chart.draw(data, options);
				}
				</script>
				''' % (i, outerl, i))

		elif q[i]["type"]=="ratingscale":
			outerl = [['Rating', 'Number']]
			minr = int(q[i]["scale"][0])
			maxr = int(q[i]["scale"][1])
			numofr = maxr - minr + 1
			#print("%d %d %d<br>" %(minr, maxr, numofr))
			for j in xrange(0, numofr):
				innerl = []
				innerl.append(str(j))
				c.execute('select answer from answer where qid="%d"' % qid)
				ans = c.fetchall()
				howmanyofthisrating = 0
				for row in ans:
					tempans = json.loads(row[0])
					#print("%s" % tempans[i]["answer"])
					if int(tempans[i]["answer"]) == (minr + j):
						howmanyofthisrating = howmanyofthisrating + 1
				if numdone == 0 or howmanyofthisrating == 0:
					tempstat = 0
				else: 
					tempstat = (float(howmanyofthisrating) / float(numdone))
				percentage = float(tempstat) * 100.0
				innerl.append(howmanyofthisrating)
				outerl.append(innerl)
				#percentage = (float(howmanyofthisrating) / float(numdone)) * 100.0
				print("<span style=\"font-size:18px\">%d people rated %s (%.1f%%)</span><br>" % (howmanyofthisrating, (minr + j), percentage))
			print('''
				<div id="piechart%d"></div>
				<script type="text/javascript">
				google.charts.load('current', {'packages':['corechart']});
				google.charts.setOnLoadCallback(drawChart);

				function drawChart() {
					var data = google.visualization.arrayToDataTable(%s);

 				// Optional; add a title and set the width and height of the chart
 				var options = {'width':550, 'height':400};

				// Display the chart inside the <div> element with id="piechart"
				var chart = new google.visualization.PieChart(document.getElementById('piechart%d'));
				chart.draw(data, options);
				}
				</script>
				''' % (i, outerl, i))

		print("<br><br>")
	print("</div>")

htmlTop()
get_cookie()

body()

#get_cookie()
htmlTail()