#  coding: utf-8
import socketserver
import socket
import mimetypes
import re
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
# Path extraction code (line 38-42): https://stackoverflow.com/questions/35555427/how-to-extract-url-from-get-http-request
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024).strip().decode()

        pattern = re.compile("^GET (.*)[ ].*")
        try:
            #get path from GET request
            line=self.data
            path = pattern.match(line).group(1)
            print ("Got a request of: %s\n" % self.data)
        except Exception as e:
            #request cannot be handled
            response = 'HTTP/1.0 305 Method Not Allowed \n\n'
            path=""
            self.request.sendall(response.encode())
            return

        if(path is "/"):
            path="/index.html"
        path="www"+path
        print(path)
        type=mimetypes.guess_type(path, strict=True)
        print(type)
        #send response
        try:
            fin = open(path)
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 200 OK\r\n'+'Content-Type: '+type[0]+'\r\n\r\n' + content
            self.request.sendall(response.encode())
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
            self.request.sendall(response.encode())
            return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

# Close socket

    server.serve_forever()
