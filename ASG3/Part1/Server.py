import socket
import os
import datetime
import psutil
credentials = {
    "mafia": "mafia",
    "basant": "localhost",
    "arch": "penguin",
    "Admin": "root"
}

last_login_file = "last_login.txt"

def authenticate_username(input_username):
    return input_username in credentials

def authenticate_password(username, input_passwd):
    return credentials.get(username) == input_passwd

def execute_command(command):
    try:
        result = os.popen(command).read()
        return result
    except Exception as e:
        return f"Command Execution Error: {str(e)}"

#
def fetch_system_info():
    memory_usage = psutil.virtual_memory().percent
    processes = psutil.cpu_count(logical=False)
    ipv4_address = socket.gethostbyname(socket.gethostname())
    last_access_time = datetime.datetime.now().strftime("%a %d-%m-%y %H:%M:%S")
    print(f"Client Connection successful ")
    print("System Information")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Processes: {processes}")
    print(f"IPv4 Address: {ipv4_address}")
    print(f"Last Access: {last_access_time}")

    return f"\nWelcome to my server:)\n"

def update_last_login():
    with open(last_login_file, 'w') as file:
        file.write(datetime.datetime.now().strftime("%a %d-%m-%y %H:%M:%S"))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = int(input("Enter the port number: "))
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(1)

    print("Establishing secure connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Authentication
    input_username = client_socket.recv(1024).decode('utf-8')
    if authenticate_username(input_username):
        client_socket.send(b'yes')

        input_passwd = client_socket.recv(1024).decode('utf-8')
        if authenticate_password(input_username,input_passwd):
            client_socket.send(b'yes')

            update_last_login()

            welcome_msg = fetch_system_info()
            client_socket.send(welcome_msg.encode('utf-8'))

        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if command == 'exit':
                print("Client disconnected\nBye.")
                break
                # continue

            if command.startswith('cd '):
                os.chdir(command[3:])
                client_socket.send(b'Directory changed.')
            elif command.startswith('mkdir '):
                os.mkdir(command[6:])
                client_socket.send(b'Directory created.')
            elif command.startswith('touch '):
                open(command[6:], 'a').close()
                client_socket.send(b'File created.')
            elif command.startswith('cat '):
                try:
                    with open(command[4:], 'r') as file:
                        content = file.read()
                        client_socket.send(content.encode('utf-8'))
                except FileNotFoundError:
                    client_socket.send(b'File not found.')
            elif command.startswith('echo '):
                try:
                    content = command[5:]

                    if ' > ' in content:
                        parts = content.split(' > ', 1)
                        file_name = parts[-1].strip()
                        with open(file_name, 'w') as file:
                            file.write(parts[0])
                        client_socket.send(b'Content updated.')
                    else:
                        client_socket.send(content.encode('utf-8'))
                except Exception as e:
                    client_socket.send(f'Error: {str(e)}'.encode('utf-8'))
            elif command.startswith('ls') or command.startswith('echo'):
                output = execute_command(command)
                client_socket.send(output.encode('utf-8'))
            else:
                client_socket.send(b'Still learning new commands')

        else:
            client_socket.send(b'no')
            print("Client disconnected")
    else:
        client_socket.send(b'no')
        print("Authentication Failed:(")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()

