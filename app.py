#! /usr/bin/env python

import BaseHTTPServer
import CGIHTTPServer
import webbrowser
import sqlite3

PORT = 8080

script_path = "cgi-bin/index.py"

server_class = BaseHTTPServer.HTTPServer
handler_class = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", PORT)

httpd = server_class(server_address, handler_class)

url = 'http://localhost:{0}/{1}'.format(PORT, script_path)

httpd.serve_forever()