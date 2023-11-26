import socket

hostname = socket.gethostname()
IPA = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port=int(input("Enter port number: "))
addr = (IPA, port)

c = "Y"
transaction_id = 1

while c.upper() == "Y":
    req_domain = input("Enter domain name: ")
    data_to_send = req_domain 
    send = s.sendto(data_to_send.encode(), addr)
    # data_another =transaction_id
    # send_another=s.sendto(data_another.encode(),addr)
    data, address = s.recvfrom(1024)
    reply_ip = data.decode().strip()
    print(f"{transaction_id} {req_domain} {reply_ip}")
    transaction_id += 1
    c = input("Continue? (y/n) ")

s.close()


