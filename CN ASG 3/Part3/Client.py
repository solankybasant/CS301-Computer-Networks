import socket
import sys
import datetime
import time

if (len(sys.argv) != 6):
    print("To use this file, run the file in the following manner:")
    print("python3 part3_client.py <localhost/ip6-localhost> <port> <packet_count> <interval> <packet_size>")
    exit()
# Hostname received from the user (localhost or ip6-localhost)
host = sys.argv[1]
# Packet count from the user
packet_count = int(sys.argv[3])
# Interval between the packets transmission
interval = int(sys.argv[4])
# Packet Size from the user
packet_size = int(sys.argv[5])

# port number of the client (hardcoded)
port = 8000
timeout = 1

# If packet size is greater than 1024 then 
if (packet_size > 1024):
    print("Packet Size should be lower than 1024")
    exit()

# UDP client Socket Initialised
UDPClientSocket = socket.socket(family=socket.getaddrinfo(host,port)[0][0], type=socket.SOCK_DGRAM)

loss_count = 0
received_count = 0
total_packets = packet_count
total_time = 0

# Run the loop for all the packet count
while (packet_count):

    # Message To send
    message = "z"*packet_size
    packet_received = False # Flag to check receiving of the file
    UDPClientSocket.sendto(bytes(message,'ascii'),(host,int(sys.argv[2])))
    start_time = datetime.datetime.now() # Start time flag
    while ((datetime.datetime.now() - start_time).total_seconds() < timeout):
        if (UDPClientSocket.recvfrom(packet_size)):
            end_time = datetime.datetime.now() # End time flag
            packet_received = True
            print(f"RTT => {(end_time - start_time).total_seconds()}")
            print("==========================")
            total_time += (end_time - start_time).total_seconds()
            received_count += 1
            break
    if (packet_received == False):
        print("Packet Loss")
        print("=======================")
        loss_count += 1
    packet_count = packet_count - 1
    time.sleep(interval)
print("======== Overall Details ========")
print(f"Packet Received: {received_count}")
print(f"Packet Sent: {total_packets}")
print(f"Loss: {(loss_count/total_packets)*100}%")
print(f"Average RTT: {total_time/total_packets}")