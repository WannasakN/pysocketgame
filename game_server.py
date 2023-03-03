import socket
import selectors
import types
import random

class GameNumber:
    MAX_ATTEMPTS = 10

    def __init__(self):
        self.answer = random.randint(1, 100)
        self.state = "Start"

    def play(self, user_input):
        if self.state == "Start":
            self.state = "Play"
        elif self.state in ["TooHigh", "TooLow"]:
            self.state = "Play"

        if self.MAX_ATTEMPTS == 0 :
            return 'You exceeded the maximum number of attempts. Game over.'
        
        elif user_input == self.answer:
            self.state = "CorrectAnswer"
            return "Correct! \nGame End , See you next time."

        elif user_input > self.answer:
            self.state = "TooHigh"
            self.MAX_ATTEMPTS -= 1
            return "It's less than that."
        
        elif user_input < self.answer:
            self.state = "TooLow"
            self.MAX_ATTEMPTS -= 1
            return "It's more than that."

sel = selectors.DefaultSelector()

host, port = '127.0.0.1', 9999
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()  
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", game=None)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)