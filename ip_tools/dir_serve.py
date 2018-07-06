
"""

Simple Static Server HTML/JS/CSS

Usage: ./dir_serve.py

Notes: serves the contents of folder '/user/desktop/html/' on port 8000

"""

# todo: make it work again

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
 
 
class StaticServer(BaseHTTPRequestHandler):
 
    def do_GET(self):
        # root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'html')
        root = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\html'

        print(self.path, " Path," + root, " root")
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
        try:
            with open(filename, 'rb') as fh:
                html = fh.read()
                # html = bytes(html, 'utf8')
                self.wfile.write(html)
        except:
            print("[-] Error: Error: Error")


def run(server_class=HTTPServer, handler_class=StaticServer, port=8000):

    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print('[+] Starting Python Folder Server on port {}'.format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[-] Closing the Python Folder Server on port %s" % port)
        exit(0)


def main():
    run()


if __name__ == '__main__':
    # call the main function
    main()
