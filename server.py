import threading
import socket

host = "127.0.0.1"  # localhost
port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chatroom'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'{str(address)} connected')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of this client is {nickname}')
        broadcast(f'{nickname} has landed in the chatroom'.encode('ascii'))
        client.send('Connected to the chatroom'. encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is starting...')
print('Server is now listening...')
receive()