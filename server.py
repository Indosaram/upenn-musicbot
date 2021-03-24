import os

from http.server import CGIHTTPRequestHandler, HTTPServer

handler = CGIHTTPRequestHandler
handler.cgi_directories = ['/']  # this is the default
server = HTTPServer(('', int(os.environ['PORT'])), handler)
server.serve_forever()