import socket
import credentials


def create_socket_client(host, port):
    socket_client = socket.socket()
    socket_client.connect((host, port))
    socket_client.send("hola desde el cliente".encode('utf-8'))
    result = socket_client.recv(1024)
    print(result)
    socket_client.close()


if __name__=='__main__':
    host = credentials.HOST_CLIENT
    port = credentials.STREAM_SOCKET_PORT
    buffer_size = credentials.BUFFER_SOCKET_SIZE
    create_socket_client(host, port)