import tweepy
import sys
import json

class TweetStreaming(tweepy.Stream):

    def set_socket(self, sock, buffer_size):
        self.sock = sock
        self.buffer_size = buffer_size
        print("Socket set")

    def on_error(self, status):        
        print(status)
        if status == 420:
            print("Too soon reconnected, Exiting!!")
            return False
        sys.exit()
        
    def on_data(self, data):
        print('\n DATA \n')
        try:
            
            data = json.loads(data)   
            # data = json.dumps(data)
            self.sock.sendall(bytes(data['text'], encoding='utf-8'))
            data = self.sock.recv(self.buffer_size)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    def on_timeout(self):
        print("Timeout")
        return True

    def on_disconnect(self, notice):
        print("Disconnected")
        return True
    



        

    
    