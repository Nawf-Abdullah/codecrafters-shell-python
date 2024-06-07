# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221))


    client,addr  = server_socket.accept()
    client.send("HTTP/1.1 200 OK\r\n\r\n]".encode("utf-8"))
    client.close()


if __name__ == "__main__":
    main()
