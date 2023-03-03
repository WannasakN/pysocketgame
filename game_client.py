import socket

HOST = "127.0.0.1"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server.")
    
    while True:
        try:
            print('-'*20)
            user_input = int(input("Enter a number between 1 and 100: "))
            if not 1 <= user_input <= 100:
                print("Input out of range. Please enter a number between 1 and 100.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")
            continue
        
        s.sendall(str(user_input).encode())
        data = s.recv(1024).decode().strip()
        print(data)
        if data == "Correct! \nGame End , See you next time.":
            break
        if data == "You exceeded the maximum number of attempts. Game over.":
            break
        