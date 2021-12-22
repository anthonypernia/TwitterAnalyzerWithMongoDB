import socket
import credentials
import json

def create_socket(host, port):
    socket_tcp =  socket.socket()
    socket_tcp.bind((host, port)) 
    socket_tcp.listen(5) 
    try:
        client, address = socket_tcp.accept()
        while True:
            data = client.recv(1024)
            data = data.decode('utf-8')
            if not data:
                break
            print(data)
            client.send(data.encode('utf-8'))
            
    except KeyboardInterrupt:
        print("Closing socket")
        socket_tcp.close()
    
    
if __name__=='__main__':
    host = credentials.HOST_CLIENT
    port = credentials.STREAM_SOCKET_PORT
    buffer_size = credentials.BUFFER_SOCKET_SIZE
    # socket_tcp =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    create_socket(host, port)
