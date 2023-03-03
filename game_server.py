import socket
import selectors
import types
import random
from colored import fg 

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
    print(f"{fg(10)}{'-'*40} \nAccepted connection from {addr} \n{'-'*40}")
    print(' ')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", game=None)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  
        if recv_data:
            if not hasattr(data, 'game') or data.game is None:
                data.game = GameNumber()
            try:
                user_input = int(recv_data.strip())
            except ValueError:
                return

            result = data.game.play(user_input)
            data.outb += result.encode('utf-8') + b'\n'
        else:
            print(f"{fg(1)}{'-'*40} \nClosing connection to {data.addr} \n{'-'*40}")
            print(' ')
            sel.unregister(sock)
            sock.close()
            
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if not data.outb.decode('utf-8').endswith('Game End , See you next time.\n') or not data.outb.decode('utf-8').endswith('Game over.\n'):
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
            else:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()