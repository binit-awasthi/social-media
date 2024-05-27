import socket
import threading
import os

SERVER_IP = "localhost"
PORT = 9000


nickName = input("enter a nickname: ")

choice = ""

while choice != "1" and choice != "2":
    os.system("cls" if os.name == "nt" else "clear")
    print("OPTIONS: ")
    print("1. localhost connection")
    print("2. remote connection")
    choice = input("Choose an option: ")
    if choice == "1":
        break
    elif choice == "2":
        SERVER_IP = input("Enter server IP: ")
        PORT = int(input("Enter server port: "))
        break

os.system("cls" if os.name == "nt" else "clear")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


client.send(nickName.encode())


lock = threading.Lock()


def closeSocket():
    global lock
    lock.acquire()
    client.close()
    lock.release()


def recvMsg():
    try:
        msg = client.recv(1024)

    except:
        print("error sending message!")

        lock.acquire()
        client.close()
        lock.release()


stop_threads = False


def closeSocket():
    global stop_threads
    stop_threads = True
    client.close()


def recvMsg():
    while not stop_threads:
        try:
            msg = client.recv(1024).decode("")
            if not msg:
                break
            print(msg)
        except:
            if not stop_threads:
                print("Error receiving message!")
            break
    closeSocket()


receivingThread = threading.Thread(target=recvMsg)
receivingThread.start()


while True:
    try:
        msg = input("Enter a message: ")
        if msg.lower() == "exit":
            closeSocket()
            receivingThread.join()
            break
        client.send(msg.encode("utf-8"))
    except Exception as e:
        print(f"Error sending message: {e}")
        closeSocket()
        receivingThread.join()
        break
