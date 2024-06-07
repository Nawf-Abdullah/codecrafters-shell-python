# Uncomment this to pass the first stage
import socket


def main():
    server_socket = socket.create_server(("localhost", 4221))


    client,addr  = server_socket.accept()
    data = client.recv(1024)

    decoded_data = data.decode().split("\r\n")

    response = b"HTTP/1.1 200 OK\r\n\r\n"

    if decoded_data[0].split(" ")[1] != "/":
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    client.sendall(response)
    client.close()


if __name__ == "__main__":
    main()
