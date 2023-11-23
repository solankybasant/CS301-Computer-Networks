import socket
import sys

if (len(sys.argv) != 3):
    print("To use this file:\n python3 part3_server.py <localhost/ip6-localhost> <port>")
    exit()

# Host received from the user
host = sys.argv[1]
# Port number received from the user 
port = sys.argv[2]
buffsize = 1024

# Get the information about the host using getaddrinfo
addr_info = socket.getaddrinfo(host,port)
# Created a UDP socket using the family info received from getaddrinfo
UDPServerSocket = socket.socket(family=addr_info[0][0], type=socket.SOCK_DGRAM)
# Binding the server to the address received from the getaddrinfo
UDPServerSocket.bind(addr_info[0][4])

if (host == "ip6-localhost"):
    print("UDP ipv6 server is running!")
else:
    print("UPD ipv4 server is running")

while (True):
    # Message and Address(client's) recevied from the client
    message,address = UDPServerSocket.recvfrom(buffsize)
    # Send the message back to the client 
    UDPServerSocket.sendto(message,address)
