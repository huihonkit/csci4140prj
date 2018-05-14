import cgi
import cgitb
import sqlite3
import json


def htmlTop():
	print("Content-type:text/html\n\n")
	print("<!DOCTYPE html>")
	print("<html lang='en'>")
	print("<head>")
	print("<meta charset='utf-8'/>")
	print("<title>prj</title>")
	print('<script src="/js/bootstrap.min.js"></script>')
	print('<link type="text/css" rel="stylesheet" href="/css/bootstrap.min.css" />')
	print('<link type="text/css" rel="stylesheet" href="/css/style1.css" />')
	print('<script src="/js/jquery-3.3.1.min.js"></script>')	
	print("</head>")
	print("<body>")

def htmlTail():
	print("</body>")
	print("</html>")


def createTable():
	conn = sqlite3.connect('test.db')
	c = conn.cursor()
	form=cgi.FieldStorage()
	qid = form.getvalue('targetQ')	
	c.execute("SELECT question from question where qid='%d'"%(int(qid)))
	questions=c.fetchone()
	questions=json.loads(questions[0])
	print('''
		<div class="container">  
  <div class="table-responsive">          
  <table class="table table-hover table-bordered table-responsive">
    <thead>
      <tr>
        <th>#</th>              
		''')
	for q in questions:		#print header
		print("<th>%s</th>"%q["question"])
	print("<th>Complete Time</th>")
	print('''</tr>
    	</thead>''')
	
	c.execute("SELECT answer from answer where qid='%d'"%(int(qid)))
	i=1
	answers=c.fetchall()
	print('<tbody>')
	for answer in answers:		
		answer=json.loads(answer[0])						
		print('<tr>')
		print('<td>%d</td>'%i)
		for a in answer:
			print('<td>%s</td>'%a["answer"])
		c.execute("SELECT time from answer where qid='%d'"%(int(qid)))
		t = c.fetchone()
		print('<td>%s</td>'%t[0])
		print('</tr>')
		i+=1	
	print('''		</tbody>
				</table>
			</div>
		</div>
		''')



