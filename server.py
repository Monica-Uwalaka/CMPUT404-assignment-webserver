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

    status_codes = {
        200: "OK",
        404: "Not Found",
        501: "Not Implemented",
    }

    
    def status_line(self, status_code):
        reason = self.status_codes[status_code]
        status_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)

        # convert str to bytes
        return status_line

    
    def handle_GET(self, request):


        path = request.request_uri # remove slash from URI
        path_arr =  request.request_uri.split("/")
        print(path_arr)
        print(path)
        #check if path exists 

        if len(path_arr[1])> 0:

            if os.path.exists(path) :
                
                #check if it is a directory
                if os.path.isdir(path):
                    #do nothing
                    if path.find("deep") == -1:
                        #serve www files
                        print("something")
                        
                    else: 
                        print("Tring to serve the deep")
                        #serve "www/deep"
                        


                    

                #if path is a files instead
                elif os.path.isfile(path):
                    #check Mimetype
                    status_line = self.status_line(200)
                    content_type = mimetypes.guess_type(path)[0]
            

                    response = status_line + "Connection: close\r\n" f"Content-Type: {content_type} \r\n" + "\r\n"
                    
                    return(response.encode())
                    
                    
                else:
                    print("not a directory")
                    #throw 404 error because file is not found/ cannot access this file

            else:
                content_type = mimetypes.guess_type(path)[0]
                
                if content_type == "text/html" or  content_type == "text/css":
            
                    not_found = "200 OK NOT FOUND!"
                    status_line = f"HTTP/1.1 200 {not_found} \r\n"
                    response = status_line + "Connection: close\r\n" + f"Content-Type: {content_type}" + "\r\n"
                    return(response.encode())
                else:
                    not_found = "404 NOT FOUND!"
                    status_line = f"HTTP/1.1 404 {not_found} \r\n"
                    response = status_line + status_line + "Connection: close\r\n" + f"Content-Type: {content_type}" + "\r\n"
                    return(response.encode())
                    
                    

            #if path is a file


        else:
            not_found = "200 OK NOT FOUND!"
            status_line = f"HTTP/1.1 200 {not_found} \r\n"
            response = status_line + "Connection: close\r\n"  + "\r\n"
            return(response.encode())


            # #You cannot access these files
            # #404 error
            # content_type = mimetypes.guess_type(path)[0]
            # if content_type == "text/html" or  content_type == "text/css":
            #     not_found = "200 OK NOT FOUND!"
            #     status_line = f"HTTP/1.1 200 {not_found} \r\n"
            #     response = status_line + "Connection: close\r\n"  + "\r\n"
            #     return(response.encode())
            # else:
            #     not_found = "400 NOT FOUND!"
            #     status_line = f"HTTP/1.1 400 {not_found} \r\n"
            #     response = status_line + "Connection: close\r\n"  + "\r\n"
            #     return(response.encode())
                
                
        

        

        

      
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
       
        #store the parsed HTTP request in a variable
        request = HTTPRequest(self.data)

        try:
            #construct the handle method for the request method
            handler = getattr(self, "handle_%s" % request.request_method)
        except:
           # handler = self.HTTP_501_handler
           pass


        #handler(request)
        response = handler(request)
        print(response)
        self.request.send(response)

      
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
