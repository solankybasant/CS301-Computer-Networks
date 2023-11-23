import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=int(input("Enter the port number:- "))
client_socket.connect(('127.0.0.1', port))


username = input("Enter Username: ")
password = input("Enter password: ")



client_socket.send(username.encode('utf-8'))

auth_response = client_socket.recv(3).decode('utf-8')


if auth_response == 'yes':
    client_socket.send(password.encode('utf-8'))
    auth_response1 = client_socket.recv(3).decode('utf-8')
    
    if auth_response1 == 'yes':
        # Display system information 
        welcome_message = client_socket.recv(1024).decode('utf-8')
        print(welcome_message)

        while True:
            command = input(f"{username}@remoteserver$ ")
            client_socket.send(command.encode('utf-8'))

            if command == 'exit':
                break

            # Receive and display the command output
            output = client_socket.recv(1024).decode('utf-8')
            print(output)
    
    else:
        print("Authentication failed")

else:
    print("Authentication failed")

client_socket.close()

