import socket
import threading
import cryptography

from cryptography.fernet import Fernet
#https://libraries.io/pypi/cryptography

IP = "127.0.0.1"
#IP = "192.168.1.88"
PORT = 8080

# create a TCP/IP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind((IP, PORT))
serverSocket.listen()

print(f'Server started on {IP}:{PORT}')

def FernetDecrypt(key, message):
    fernet = Fernet(key)
    return fernet.decrypt(message).decode()

def broadcast(message):
    print(f'Server: Clients to broadcast message to all clients in chatroom: {[v for v in clientMappings.values()]}')
    for client in clients:
        client.send(message)

def handleClient(clientSocket, clientAddress, clientMappings):

    print(f'Server: Accepted connection from a client {clientAddress[0]}:{clientAddress[1]}')
    key = clientSocket.recv(1024).decode()
    print(f"Server: Key received from client: {key}")
    try:
        clientName = FernetDecrypt(key, clientSocket.recv(1024))
        print(f'Server: Client {clientAddress[0]}:{clientAddress[1]} has adopted username: {clientName}')
        
    except ConnectionResetError:
        print(f'Server: The client {clientAddress[0]}:{clientAddress[1]} has disconnected')
        return None
    
    if clientName == "QUIT":
        print(f'Server: The client {clientAddress[0]}:{clientAddress[1]} has disconnected')
        return None
    
    try:
        clientSocket.send(f"Good afternoon, {clientName}!\nSay something!".encode())

    except ConnectionResetError:
        print(f'Server: The client has abruptly disconnected!')
        return None
    
    if len(clients) > 0:

        print(f'Server: Message to broadcast: {clientName} has joined the chat room!')
        broadcast(f'{clientName} has joined the chat room!'.encode())
    
    clientMappings[clientAddress] = clientName
    name = clientName
    clients.append(clientSocket)
    while True:
        try:
            message = FernetDecrypt(key, clientSocket.recv(1024))
        except cryptography.fernet.InvalidToken:
            clients.remove(clientSocket)
            print(f'Server: The client {clientAddress[0]}:{clientAddress[1]} ({clientMappings.get(clientAddress)}) has disconnected.')
            del clientMappings[clientAddress]
            broadcast(f'\n{name} has disconnected from the chat room.\n'.encode())
            break


        if message == "QUIT":
            
            clients.remove(clientSocket)
            print(f'Server: The client {clientAddress[0]}:{clientAddress[1]} ({clientMappings.get(clientAddress)}) has disconnected.')
            del clientMappings[clientAddress]
            broadcast(f'\n{name} has disconnected from the chat room.\n'.encode())
            break

        print(f'Server: Message from {clientAddress[0]}:{clientAddress[1]} ({clientMappings.get(clientAddress)}): {message}.')
        print('Server: Broadcasting message...')

        broadcast(f'{clientMappings.get(clientAddress)} says: {message}'.encode())
        
clients = []
clientMappings = {}

while True:
    # wait for a client connection
    clientSocket, clientAddress = serverSocket.accept()
    # start a new thread to handle the client connection
    clientThread = threading.Thread(target=handleClient, args=(clientSocket, clientAddress, clientMappings))
    clientThread.start()