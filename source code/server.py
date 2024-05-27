import socket
import threading

SERVER_IP = "localhost"
PORT = 9000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))

server.listen()
print(f"server listening on port {PORT}...")

clients = []


def broadcast(msg, client):
    for cl in clients:
        if cl != client:
            cl.send(msg)


def handleClient(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)

        except:
            index = clients.index(client)
            clients.remove(client)
            broadcast(f"client{index} left".encode(), client)
            client.close()
            print(f"client{index} left")
            break


def acceptClient():
    while True:
        try:
            client, addr = server.accept()
            client.send(f"welcome".encode())

            clients.append(client)

            msg = f"client{clients.index(client)} joined."
            print(msg)
            broadcast(msg.encode(), client)

            thread = threading.Thread(target=handleClient, args=(client,))
            thread.start()

        except:
            break


acceptClient()

print("shutting the server down...")
server.close()