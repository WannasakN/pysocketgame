import socket
from colored import fg,attr

HOST = "127.0.0.1"
PORT = 9999

def connect_to_server( HOST, PORT ):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try :
            s.connect((HOST, PORT))
        except:
            print(f"{fg(1)}Can\'t connect to server, server is not available or something wrong happened{attr(0)}")
            return 
        print("Connected to server.")
        
        while True:
            try:
                print('-'*20)
                user_input = int(input("Enter a number between 1 and 100: "))
                if not 1 <= user_input <= 100:
                    print(f"{fg(1)}Input out of range. Please enter a number between 1 and 100.{attr('reset')}")
                    continue
            except ValueError:
                print(f"{fg(1)} Invalid input. Please enter a number between 1 and 100.{attr('reset')}")
                continue
            
            s.sendall(str(user_input).encode())
            data = s.recv(1024).decode().strip()
            print(f'{fg(10)}{data}{attr("reset")}')
            if data == "Correct! \nGame End , See you next time.":
                break
            if data == "You exceeded the maximum number of attempts. Game over.":
                break

connect_to_server(HOST, PORT)