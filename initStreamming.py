import credentials
import socket
from StreamingListener import TweetStreaming

if __name__=='__main__':
    consumer_key = credentials.API_KEY
    consumer_secret = credentials.API_KEY_SECRET
    access_token = credentials.ACCESS_TOKEN
    access_secret = credentials.ACCESS_TOKEN_SECRET
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = credentials.HOST_CLIENT
    port = credentials.STREAM_SOCKET_PORT
    buffer_size = credentials.BUFFER_SOCKET_SIZE
    socket_tcp.connect((host, port))
    tweetStreaming = TweetStreaming(
        consumer_key, consumer_secret,
        access_token, access_secret )
    tweetStreaming.set_socket(socket_tcp, buffer_size)
    tweetStreaming.filter(track=[credentials.QUERY.strip()])
    