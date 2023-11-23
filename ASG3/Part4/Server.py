import socket
import sys
from _thread import *
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    print("Correct usage: script, port number")
    exit()
IPA = socket.gethostbyname(socket.gethostname())

Port = int(sys.argv[1])  
server.bind((IPA, Port))  # We are setting up the ip_address and port number for the server
server.listen(100)  # We can set the number of users to 100
all_clients = []


# New threads will be created for different users for this function
def clientthread(conn, addr):
    conn.send(b"Hola amigos!")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                # Get the current time
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # Print the message along with the timestamp
                print(f"({addr[0]}) [{current_time}]: {message.decode()}")

                # Calls broadcast function to send message to all
                message_to_send = f"({addr[0]}) [{current_time}]: {message.decode()}"
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


# broadcast the message to all other users
def broadcast(message, connection):
    for clients in all_clients:
        if clients != connection:
            try:
                clients.send(bytes(message, 'ascii'))
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)


def remove(connection):
    if connection in all_clients:
        all_clients.remove(connection)

while True:
    conn, addr = server.accept()  
    all_clients.append(conn)
    # prints the address of the user that just connected
    print(addr[0] + " connected")
    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread, (conn, addr))

