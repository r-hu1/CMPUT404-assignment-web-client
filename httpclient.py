#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import os
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    
    def get_host_port(self,url):
        pars = url.split('/')
        path = "/"
                
        host = pars[2]
        
        
        if len(pars)>3:
            path_parts = pars[3:]
            
            path += "/".join(path_parts)
    
        if (host.find(':') != -1):
            host, port = host.split(':')
            port = int(port)
    
        else:
            host, port = host, 80
        return host, port, path



    def connect(self, host, port):
        # use sockets!
        
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host,port))
    
        return clientSocket

    def get_code(self, data):

        try:
            data_code = int(data.split(" ")[1])
        except:
            data_code = 404
        
        return data_code



#    def get_headers(self,data):
#         return None
    

    def get_body(self, data):
        body_info = data.split("\r\n\r\n")
        if len(body_info) > 1:
            return body_info[1]
        else:
            return data


    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        
        
        
        if (args != None):
            encode = urllib.urlencode(args)
            send_all = "Content-type:application/x-www-form-urlencoded ; charset=UTF-8\r\n"
            send_all += "Content-Length: %d\r\n\r\n" %(len(encode))
            send_all += "%s\r\n" %(encode)
            send_all += "\r\n"
        else:
            send_all = "Content-type:application/x-www-form-urlencoded ; charset=UTF-8\r\n"
            send_all += "Content-Length: 0\r\n\r\n"
            send_all += "\r\n"
            send_all += "\r\n"
        
        
        host,port,file = self.get_host_port(url)
        conn = self.connect(host,port)
        
        conn.sendall("GET " + file + " HTTP/1.1\r\n")
        conn.sendall("Host: " + host + "\r\n")
        conn.sendall("Connection: close\r\n\r\n")
        conn.sendall("Accept: */*\r\n")

        conn.sendall(send_all)
        
        retutn_val = self.recvall(conn)
        code = self.get_code(retutn_val)
        body = self.get_body(retutn_val)
        
        print code
        print body
        
        conn.close()
        
    
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        if (args != None):
            encode = urllib.urlencode(args)
            send_all = "Content-type:application/x-www-form-urlencoded ; charset=UTF-8\r\n"
            send_all += "Content-Length: %d\r\n\r\n" %(len(encode))
            send_all += "%s\r\n" %(encode)
            send_all += "\r\n"
        else:
            send_all = "Content-type:application/x-www-form-urlencoded ; charset=UTF-8\r\n"
            send_all += "Content-Length: 0\r\n\r\n"
            send_all += "\r\n"
            send_all += "\r\n"
        
        
        host,port,file= self.get_host_port(url)
        conn = self.connect(host,port)

        conn.sendall("POST " + file + " HTTP/1.1\r\n")
        conn.sendall("Host: " + host + "\r\n")
        conn.sendall(send_all)
        
        retutn_val = self.recvall(conn)
        code = self.get_code(retutn_val)
        body = self.get_body(retutn_val)
        
        print code
        print body
        
        conn.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
