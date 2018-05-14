#! /usr/bin/env python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user
		(uid integer PRIMARY KEY, uname text, password text, mark integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS session
		(sid integer PRIMARY KEY, uid integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS question
		(qid integer PRIMARY KEY, uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json, num_done integer, est integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS answer
		(qid integer, uid integer, answer json, time text)''')
c.execute('''CREATE TABLE IF NOT EXISTS draft
		(did integer PRIMARY KEY, uid integer, num_question integer, use_mark integer, time date, title text, des text, category text, question json)''')
c.execute("DELETE FROM user")
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark) VALUES (?, ?, ?, ?)", (1, 'user1', 'test', 0))
conn.commit()
c.execute("INSERT INTO user(uid, uname, password, mark) VALUES (?, ?, ?, ?)", (2, 'user2', 'pw', 1000))
conn.commit()
conn.close()