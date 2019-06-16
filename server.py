#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import os
import subprocess


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def returnlist(self):				
	f = open("shoppinglist.txt","r")
	if f.mode == "r":
		contents = f.read()			
        self.wfile.write(contents[2:])			

    def writelist(self, data):				
        f = open("shoppinglist.txt", "w+")		
        f.write(data)					
        f.close()
        print('Got POST request. Received data: %s' % data)


    def do_GET(self):					
        self._set_headers()
        subprocess.call(['./imageencoder.sh'])		
        with open("b64.txt", "r") as myfile:		
            data = myfile.readlines()
        os.remove("b64.txt")
        os.remove("image.png")
        self.wfile.write(data)				


    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  	
        if post_data == "0":				
            self.returnlist()				
        else:
            self.writelist(post_data) 			

def run(server_class=HTTPServer, handler_class=S, port=8080):	
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting server...'
        print('Server running on port %d' % port)
        httpd.serve_forever()				
    except KeyboardInterrupt:
        print '\n^C received. Shutting down server.'
        httpd.socket.close()				
        print 'Server closed.'


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
