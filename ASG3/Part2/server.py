import socket

def read_dns_table(file_path):
    dns_table = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            transaction_id, domain, ip = int(parts[0]), parts[1], parts[2]
            dns_table[domain]=ip
    return dns_table

file_path = 'query'
dns_table = read_dns_table(file_path)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Server starting...")

port=int(input("Enter port number: "))
s.bind(("127.0.0.1", port))

while True:
    data, address = s.recvfrom(1024)
    print(f"{address} wants to fetch data!")
    data = data.decode()
    ip = dns_table.get(data, "Not found!").encode()
    s.sendto(ip, address)

