#!/usr/bin/env python3

"""
Simple Static Server 

Usage: ./s_server.py

Notes: serves the contents of folder '/user/desktop/html/' on port 8000
"""


from http.server import HTTPServer, BaseHTTPRequestHandler
import os
 
 
class StaticServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
        root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'html')
        # print(self.path)
        if self.path == '/':
            filename = root + '/index.html'
        else:
            filename = root + self.path
 
        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            try:
                self.send_header('Content-type', 'image/x-icon')
            except:
                # Annoying error, shitty fix.
                pass
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fh:
            html = fh.read()
            #html = bytes(html, 'utf8')
            self.wfile.write(html)


def run(server_class=HTTPServer, handler_class=StaticServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()
 
run()
