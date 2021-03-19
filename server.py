import socket
import threading

HOST = '192.168.100.24'

PORT = 2701

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []



def broadcast(message):
    for client in clients:
        client.send(message)


def handle():
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}...")


        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)


        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname} connecting...")
        broadcast(f"{nickname} has joined the room \n".encode('utf-8'))
        client.send("Connected...".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server running...")
receive()
