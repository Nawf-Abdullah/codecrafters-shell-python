# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221))

    while True:
        client,addr  = server_socket.accept()
        client.send("HTTP".encode("utf-8"))
        client.close()


if __name__ == "__main__":
    main()
