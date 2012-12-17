import socket
import time

ADDRESS = ''
PORT = 8123

class Client(object):
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((ADDRESS, PORT))
        self.ready_for_word = False
    def wait_for(self, query, message='waiting...'):
        while True:
            self.s.send(query)
            m = self.s.recv(1000)
            if m != 'False':
                print m
                break
            time.sleep(1)
            print message
    def play(self):
        self.wait_for('paired?', 'waiting for partner...')
        word = raw_input('Enter a word for your opponent to guess: ')
        self.s.send('assign '+word)
        m = self.s.recv(1000)
        self.wait_for('ready?', 'waiting for partner to give us a word...')
        while True:
            guess = raw_input('Enter a letter to guess: ')
            self.s.send('guess '+guess)
            m = self.s.recv(1000)
            print m
            if 'You win' in m:
                break
            if 'You lose' in m:
                break

if __name__ == '__main__':

    c = Client()
    c.play()
