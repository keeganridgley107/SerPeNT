"""New version of folder server for python 3"""
import http.server
import socketserver
import os
from pathlib import Path


def run():

    PORT = 8000
    home = str(Path.home())
    web_dir = os.path.join(home, '.')

    print("[+] Folder Server path is: ", web_dir)
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("[+] Serving on port ", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[-] Closing the server...")
        exit(0)


def main():
    run()


if __name__ == '__main__':
    main()
