import socket
import threading
import sys

HEADER = 2048

def receive_messages(client):
    while True:
        try:
            msg = client.recv(HEADER).decode("utf-8")
            if msg:
                print(msg)
        except:
            print("Connection lost")
            client.close()
            break

if __name__ == "__main__":
    HOST = input("Host: ")
    PORT = int(input("Port: "))

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        thread = threading.Thread(target=receive_messages, args=(client,))
        thread.start()

        print("* Connected to the server")

        while True:
            msg = input().encode("utf-8")

            if msg == "!disconnect":
                client.send(msg)
                break
            
            client.send(msg)

    except:
        print("Connection failure")
