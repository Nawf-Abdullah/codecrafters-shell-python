# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221))


    conn,addr  = server_socket.accept()
    with conn:
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
            if 'user-agent' in path[1]:
                code = args[2].strip("User-Agent: ")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(code)}\r\n\r\n{code}".encode()
                
            print(f"First par {path}")

        print(f"Received: {val}")
        conn.sendall(response)



if __name__ == "__main__":
    main()
