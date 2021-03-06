#  coding: utf-8 
import socketserver
import os
import mimetypes

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
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class HTTPRequest:
    """
    parse HTTP request 
    Input: data
    """
    def __init__(self, data):
        self.request_method = None
        self.request_uri = None
        self.http_version = '1.1'

        #parse the request data
        self.parse_request(data)

    #Parse HTTP Request
    def parse_request(self, data):
        http_request = data.split(b"\r\n")
        
        #for loop to print and decode the client request on the server   
        for i in range(len(http_request)):
            http_request[i] = http_request[i].decode("utf-8")
            print(http_request[i])

        request_line = http_request[0]
        
        #split self.request_line by space
        request_line = request_line.split(" ")
        
        self.request_method = request_line[0]

        #check if request_line contains a uri and http_version
        if len(request_line) > 1:
            self.request_uri = request_line[1]

        if len(request_line) > 2:
            self.http_version = request_line[2]

        



class MyWebServer(socketserver.BaseRequestHandler):
    
   

   
        
    def get_200(self, path):
        content_type = mimetypes.guess_type(path)[0]
        not_found = "200 OK NOT FOUND!"
        status_line = f"HTTP/1.1 200 {not_found} \r\n"
        response = status_line + "Connection: close\r\n" + f"Content-Type: {content_type}" + "\r\n" + "\r\n"
        return(response.encode())

    def get_404(self, path):
        content_type = mimetypes.guess_type(path)[0]
        not_found = "404 NOT FOUND!"
        status_line = f"HTTP/1.1 404 {not_found} \r\n"
        response = status_line + "Connection: close\r\n" + f"Content-Type: {content_type}" + "\r\n" + "\r\n"
        return(response.encode())


    def get_405(self, path):
        content_type = mimetypes.guess_type(path)[0]
        not_found = "405 NOT FOUND!"
        status_line = f"HTTP/1.1 405 {not_found} \r\n"
        response = status_line + "Connection: close\r\n" + f"Content-Type: {content_type}" + "\r\n" + "\r\n"
        return(response.encode())

    def get_301(self, path):
        path = path + "index.html"
        content_type = mimetypes.guess_type(path)[0]
        not_found = "301 Moved Permanently!"
        status_line = f"HTTP/1.1 301 {not_found} \r\n"
        response = status_line + f"Location: {path}" + "\r\n" + f"Content-Type: {content_type}" + "\r\n" + "\r\n"
        return(response.encode())

    def secure(self, path):

        if path.find("/.") == -1 and path.find("/..") == -1:
            return True
        else:
            return False
            

        

    #FROM: https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/
    def handle_GET(self, request):

        path = request.request_uri # remove slash from URI

        cpath = path.strip('/')

        path = "www" + path

       

        if  self.secure(path):

            if not cpath:
                path = "www/index.html"
                with open(path, 'rb') as f:
                    message_body = f.read()
                response = self.get_200(path)
                print(response)
                self.request.send(response)
                self.request.send(message_body)
                self.request.send(b"\r\n")

          
            if os.path.exists(path) :
               
                if os.path.isdir(path) or os.path.isdir(path + "/") :

                    if cpath[-1] == "":
                       
                        path = path  + "/index.html"
                        with open(path, 'rb') as f:
                            message_body = f.read()
                        response = self.get_301(path)
                        self.request.send(response)
                        self.request.send(b"\r\n")

                    else:
                        path = path  + "/index.html"
                        print("path")
                        with open(path, 'rb') as f:
                            message_body = f.read()
                        response = self.get_200(path)
                        print(response)
                        self.request.send(response)
                        self.request.send(message_body)
                        self.request.send(b"\r\n")
                else:
                    with open(path, 'rb') as f:
                        message_body = f.read()
                    response = self.get_200(path)
                    print(response)
                    self.request.send(response)
                    self.request.send(message_body)
                    self.request.send(b"\r\n")
        
        
            else:
                response = self.get_404(path)
                print(response)
                self.request.send(response)
                self.request.send(b"\r\n")
        else:
            response = self.get_404(path)
            print(response)
            self.request.send(response)
            self.request.send(b"\r\n")

    def handle_PUT(self, request):
        path = request.request_uri # remove slash from URI

        cpath = path.strip('/')

        path = "www" + path

        if not cpath:
            path = "www/index.html"
            #FROM:https://stackoverflow.com/users/1222951/aran-fey
            #URI to question: https://stackoverflow.com/questions/53204752/how-do-i-read-a-text-file-as-a-string/53204836#53204836
            with open(path, 'rb') as f:
                message_body = f.read()
            response = self.get_200(path)
            print(response)
            self.request.send(response)
            self.request.send(message_body)
            self.request.send(b"\r\n")

        
        if os.path.exists(path):
            if os.path.isdir(path):
                path = path + "index.html"
            
                print("path")
                with open(path, 'rb') as f:
                    message_body = f.read()
                response = self.get_200(path)
                print(response)
                self.request.send(response)
                self.request.send(message_body)
                self.request.send(b"\r\n")
            elif os.path.isdir(path + "/"):
                redirect_path = path + "/"
                response = self.get_301(redirect_path)
                print(response)
                self.request.send(response)
                self.request.send(b"\r\n")

            else:
                if mimetypes.guess_type(path)[0] != "text/html":
                        response = self.get_405(path)
                        print(response)
                        self.request.send(response)
                        self.request.send(b"\r\n")
                    
                else:
                    with open(path, 'rb') as f:
                        message_body = f.read()
                    response = self.get_200(path)
                    print(response)
                    self.request.send(response)
                    self.request.send(message_body)
                    self.request.send(b"\r\n")
    
       
        else:
            response = self.get_405(path)
            print(response)
            self.request.send(response)
            self.request.send(b"\r\ n")

        
        
        

      
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
       
        #store the parsed HTTP request in a variable
        request = HTTPRequest(self.data)

         #FROM: https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/
        try:
            #construct the handle method for the request method
            handler = getattr(self, "handle_%s" % request.request_method)
        except:
           pass


        #handler(request)
        handler(request)
        # print(response)
        # self.request.send(response)

      
        # print(self.request_method)
        #print ("Got a request of: %s\n" % response)
        #self.request.sendall(bytearray("OK",'utf-8'))

   
        

  

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
server.serve_forever()
