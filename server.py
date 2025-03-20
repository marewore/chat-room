import socket
import threading

HEADER = 2048
HOST = socket.gethostbyname(socket.gethostname())
PORT = int(input("Listening port: "))

clients = {} 

def broadcast(message, sender_conn):
    for conn in clients.keys():
        if conn != sender_conn:
            try:
                conn.send(message)
            except:
                conn.close()
                del clients[conn]

def client_thread(conn, addr):
    print(addr, "Connected to the server.")
    clients[conn] = addr

    connected = True
    while connected:
        try:
            msg = conn.recv(HEADER)
            if msg:
                if msg.decode("utf-8") == "!disconnect":
                    connected = False
                    break

                print(f"<{addr}> {msg.decode('utf-8')}")
                broadcast(msg, conn)
        except:
            break

    conn.close()
    del clients[conn]
    print(f"{addr} Disconnected.")

def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Server is listening on {HOST}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()
    except:
        print("Connection failure")

if __name__ == "__main__":
    print("Server starting...")
    main()