import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
	print ("Correct usage: script, port number")
	exit()
IPA = socket.gethostbyname(socket.gethostname())

Port = int(sys.argv[1])
server.connect((IPA, Port))

while True:

	# maintains a list of possible input streams
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print(f"Received Message: {message}")
		else:
			message = sys.stdin.readline()
			server.send(bytes(message,'ascii'))
			sys.stdout.write("<User>")
			sys.stdout.write(message)
			sys.stdout.flush()


