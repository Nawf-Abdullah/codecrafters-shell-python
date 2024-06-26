# Uncomment this to pass the first stage
import socket
import threading
import sys
from io import StringIO 
import gzip


def check_encode(encodings_list):
    valid_encoding = ['gzip']
    splited = encodings_list.split(',')
    print('SPLITTED ARRAY:',splited)
    for i in splited:
        if i.strip(' ') in valid_encoding:
            return True
    return False

def c_handler(conn,addr):
        val = conn.recv(1024)
        pars = val.decode()
        args = pars.split("\r\n")
        isEncodingAvailable = False
        for i in args:
                if i.startswith('Accept-Encoding:') and  check_encode(i.split(':')[1].strip(' ')):
                    print('Encoding value',i.split(':')[1])
                    # response = response.decode().split('\r\n')
                    # response.insert(-2,f'Content-Encoding: gzip',)
                    # response = '\r\n'.join(response).encode()
                    isEncodingAvailable = True
                    break
        # gzip.compress(bytes(exampleString, 'utf-8'))
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        if len(args) > 1:
            path = args[0].split(" ")
            if path[1] == "/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
            if "echo" in path[1]:
                string = path[1].split("/echo/")
                print('THE DIVIDED SHIT:',string)
                if not isEncodingAvailable:
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string[1])}\r\n\r\n{string[1]}".encode()
                else:
                    x = gzip.compress(bytes(string[1], 'utf-8'))
                    print('ENCODED DATA: ',x)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(x)}\r\n\r\n".encode()+x
                    
           
            elif path[1].startswith("/user-agent"):
                if args[2].startswith('User-Agent:'):
                    print("dbfbgdfg")
                    user_agent = args[2].split(": ")[1]
                else:
                    print("ggererbitvh")
                    user_agent = args[3].split(": ")[1]
                
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
                print("Agent:"+user_agent)
            elif path[1].startswith('/files') and path[0]=='GET':
                print(sys.argv)
                try:
                    print('path:',path)
                    print('The Argss:',args)
                    newp = args[0].split(" ")[1]
                    print(f'path to file : {sys.argv[2]}/{newp[7:]}')
                    with open(f'{sys.argv[2]}/{newp[7:]}') as f:
                        x = f.read()
                        print('content',x)
                        content_length = len(x)
                        if not isEncodingAvailable:
                            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n{x}".encode()
                        else:
                            encodeX =  gzip.compress(bytes(x, 'utf-8'))
                            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Encoding: gzip\r\nContent-Length: {len(encodeX)}\r\n\r\n".encode()+encodeX
                        print(x)
                except FileNotFoundError:
                    response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode()
            elif path[1].startswith('/files') and path[0]=='POST':
                print('THE ARGS ', args)
                newp = args[0].split(" ")[1]
                print(f'path to file : {sys.argv[2]}/{newp[7:]}')
                with open(f'{sys.argv[2]}/{newp[7:]}',"w") as f:
                    f.write(args[-1])
                response = 'HTTP/1.1 201 Created\r\n\r\n'.encode()
                
                #THE ARGS  ['POST /files/file_123 HTTP/1.1', 'Host: localhost:4221', 'User-Agent: curl/8.4.0', 'Accept: */*', 'Content-Type: application/octet-stream', 'Content-Length: 5', '', '12345']
            


            print(f"First par {path}")
            

        print(f"Received: {val}")
        conn.send(response)


def main():
    server_socket = socket.create_server(("localhost", 4221))

    while True:
        conn,addr  = server_socket.accept()
        threading.Thread(target=c_handler, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
