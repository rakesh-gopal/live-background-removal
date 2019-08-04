#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import face_detect
from threading import Thread
import subprocess


def threaded_function(vidurl, outid):
    face_detect.process_vid(vidurl, outid)


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        try:
            vidurl = query_components["vidurl"][0]
            outid = query_components["outid"][0]
            print('vidurl: ' + vidurl)
            thread = Thread(target=threaded_function, args=(vidurl, outid))
            thread.start()

            # subprocess.Popen('python3 face_detector.py "%s"' % vidurl[0], shell=True)
        except:
            pass

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
