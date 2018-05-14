#! /usr/bin/env python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user
		(uid integer PRIMARY KEY, uname text, password text, mark integer, credit integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS session
		(sid integer PRIMARY KEY, uid integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS question
		(qid integer PRIMARY KEY, uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json, num_done integer, est integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS answer
		(qid integer, uid integer, answer json, time text)''')
c.execute('''CREATE TABLE IF NOT EXISTS draft
		(did integer PRIMARY KEY, uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json)''')
c.execute('''CREATE TABLE IF NOT EXISTS predict
		(pid integer PRIMARY KEY, qid integer, uid integer, predict integer)''')
c.execute("DELETE FROM user")
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (1, 'admin', 'admin', 9999, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (2, 'alex', 'alex', 1000, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (3, 'betty', 'betty', 1000, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (4, 'chris', 'chris', 1000, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (5, 'david', 'david', 1000, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (6, 'eddie', 'eddie', 1000, 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark, credit) VALUES (?, ?, ?, ?, ?)", (7, 'freddy', 'freddy', 1000, 0))
conn.commit()
conn.close()
