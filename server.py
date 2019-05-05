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

    def returnlist(self):				# <--- Metoden der sender listen tilbage.
	f = open("shoppinglist.txt","r")
	if f.mode == "r":
		contents = f.read()			# <--- Læs indholdet
        self.wfile.write(contents[2:])			# <--- Send den læste data

    def writelist(self, data):				# <--- Metoden der skriver data til indkøbsliste.
        f = open("shoppinglist.txt", "w+")		# <--- Klargør listen
        f.write(data)					# <--- Skriv til listen
        f.close()
        print('Got POST request. Received data: %s' % data)


    def do_GET(self):					# <--- GET request. Når der kommer en GET request, er det fordi appen vil have et billede.
        self._set_headers()
        subprocess.call(['./imageencoder.sh'])		# <--- Kør bash script, der tager billede
        with open("b64.txt", "r") as myfile:		# <--- Læs billedet der er kodet i base64
            data = myfile.readlines()
        os.remove("b64.txt")
        os.remove("image.png")
        self.wfile.write(data)				#  <--- Send billeddataen i base64


    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  	# <--- Henter data fra POST request
        if post_data == "0":				# <--- Hvis POST data er lig "0", vil appen kun læse listen. Derfor sendes listen tilbage
            self.returnlist()				# <--- Her kaldes returnlist(), der sender listen.
        else:
            self.writelist(post_data) 			# <--- Hvis requesten indeholder andet data, skrives dette data til listen.

def run(server_class=HTTPServer, handler_class=S, port=8080):	# <--- Main metoden. Her startes serveren.
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting server...'
        print('Server running on port %d' % port)
        httpd.serve_forever()				# <--- Starter serveren, jævnførende deklarationen ovenover
    except KeyboardInterrupt:
        print '\n^C received. Shutting down server.'
        httpd.socket.close()				# <--- Slukker serveren, hvis man sender CTRL+C
        print 'Server closed.'


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
