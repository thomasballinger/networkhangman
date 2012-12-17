import socket
import select
import threading

import game

ADDRESS = ''
PORT = 8123

def run_server_daemon():
    t = threading.Thread(target=HangmanServer)
    t.daemon = True
    t.start()

class HangmanServer(object):
    def __init__(self):
        self.listener = socket.socket()
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ADDRESS, PORT))
        self.pair_mapping = {}
        self.listen_forever()

    def listen_forever(self):
        self.listener.listen(5)
        while True:
            r, w, e = select.select(self.pair_mapping.values() + [self.listener], [], [])
            for reader in r:
                if reader is self.listener:
                    (s, (addr, ip)) = self.listener.accept()
                    c = Connection(s, (addr, ip), self)
                    if None in self.pair_mapping:
                        self.pair_mapping[c] = self.pair_mapping[None]
                        self.pair_mapping[self.pair_mapping[None]] = c
                        del self.pair_mapping[None]
                    else:
                        self.pair_mapping[None] = c
                else:
                    reader.read()

class Connection(object):
    def __init__(self, s, (addr, ip), server):
        self.s = s
        self.name = addr + ':' + str(ip)
        self.read_buffer = ''
        self.game = game.Hangman()
        self.server = server
    def __repr__(self):
        return 'Connection('+repr(self.s)+', '+self.name+')'
    def fileno(self):
        return self.s.fileno()
    def __eq__(self, other):
        return self.s == other.s
    def __hash__(self):
        return hash(self.s)
    def read(self):
        """
        Reads on the connection's socket, and takes action and
        sends back response iff an entire message was received
        We assume only one message will ever arrive at a time,
        but that it's possible we won't have the whole message on this read
        """
        data = self.s.recv(1000)
        message = parse_message(self.read_buffer + data)
        if message:
            self.read_buffer = ''
            self.send(self.action(message))
    def action(self, message):
        if message == 'paired?':
            return self.game if self in self.server.pair_mapping else False
        if message == 'ready?':
            return self.game if self.game.word is not None else False
        elif message[:5] == 'guess':
            if len(message) != 7:
                print 'received bad guess message:', message
                return False
            self.game.guess(message[6])
            return self.game
        elif message[:6] == 'assign':
            try:
                cmd, word = message.split()
            except ValueError:
                print 'received bad message:', message
                return False
            if self in self.server.pair_mapping:
                self.server.pair_mapping[self].game.set_word(word)
                return self.game
            else:
                print 'tried to set word, but game is unpaired'
                return False
        else:
            print 'received bad message:', message
            return False
    def send(self, s):
        self.s.sendall(str(s))


def parse_message(data):
    """Later this will check that we've received a whole message
    for now, assume we always have"""
    return data

if __name__ == '__main__':
    s = HangmanServer()
    s.listen_forever()
