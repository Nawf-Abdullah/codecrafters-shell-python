# Uncomment this to pass the first stage
import socket
import threading
import sys


def c_handler(conn,addr):
        val = conn.recv(1024)
        pars = val.decode()
        args = pars.split("\r\n")
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        if len(args) > 1:
            path = args[0].split(" ")
            if path[1] == "/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
            if "echo" in path[1]:
                string = path[1].strip("/echo/")
                
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            # if 'user-agent' in path[1]:
            #     code = args[3].strip("User-Agent: ")
            #     response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(code)}\r\n\r\n{code}".encode()
            elif path[1].startswith("/user-agent"):
                if args[2].startswith('User-Agent:'):
                    print("dbfbgdfg")
                    user_agent = args[2].split(": ")[1]
                else:
                    print("ggererbitvh")
                    user_agent = args[3].split(": ")[1]
                
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
                print("Agent:"+user_agent)
            elif path[1].startswith('/files'):
                print(sys.argv)
                try:
                    with open(f'../tmp/{path[7:]}') as f:
                        x = f.read()
                        content_length = len(x)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{x}".encode()
                        print(x)
                except FileNotFoundError:
                    response = 'HTTP/1.1 404 Not Found\r\n\r\n'.encode()
            
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
