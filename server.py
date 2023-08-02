import socket
import threading
import datetime

MESSAGE_FILE = "messages.txt"

def handle_client_connection(conn, addr, clients):
    print(f"Verbunden mit: {addr[0]}:{addr[1]}")
    username = conn.recv(1024).decode()
    clients[conn] = username

    try:
        # Send the message history to the newly connected client
        send_message_history(conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"{clients[conn]}: {message}")

            # Get the current timestamp (hour:minute)
            current_time = datetime.datetime.now().strftime("%H:%M")

            # Weiterleiten der Nachricht an alle anderen verbundenen Clients mit Uhrzeit
            for client, name in clients.items():
                if client != conn:
                    client.sendall(f"[{current_time}] [{clients[conn]}]: {message}".encode())

            # Speichern der Nachricht in der Datei
            with open(MESSAGE_FILE, "a") as file:
                file.write(f"[{current_time}] [{clients[conn]}]: {message}\n")
    except:
        pass

    print(f"Verbindung zu {addr[0]}:{addr[1]} geschlossen.")
    del clients[conn]
    conn.close()

def send_server_message(server_socket, clients):
    while True:
        message = input("Server: ")
        # Get the current timestamp (hour:minute)
        current_time = datetime.datetime.now().strftime("%H:%M")
        # Weiterleiten der Nachricht an alle verbundenen Clients mit Uhrzeit
        for client, name in clients.items():
            client.sendall(f"[{current_time}] Server: {message}".encode())

def send_user_list(client_socket, clients):
    try:
        user_list = "\n".join(clients.values())
        client_socket.sendall(f"[Server]: Aktive Benutzer:\n{user_list}\n".encode())
    except:
        pass

def start_server():
    host = "0.0.0.0"  # Server lauscht auf allen verfügbaren IP-Adressen
    port = 12345    # Portnummer, auf dem der Server lauscht

    # Reset the message file at the start of the server
    with open(MESSAGE_FILE, "w") as file:
        file.write("Chatstart")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Chat-Server gestartet. Warte auf Verbindungen auf {host}:{port}")

    connected_clients = {}  # Wörterbuch zum Speichern der verbundenen Clients und Benutzernamen

    try:
        server_thread = threading.Thread(target=send_server_message, args=(server_socket, connected_clients))
        server_thread.start()

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr, connected_clients))
            client_thread.start()

            # Thread für das Senden der Benutzerliste an den neuen Client starten
            user_list_thread = threading.Thread(target=send_user_list, args=(conn, connected_clients))
            user_list_thread.start()

    except KeyboardInterrupt:
        # Bei einem Tastenabbruch (z. B. durch CTRL+C) den Server beenden
        pass
    finally:
        # Socket schließen, wenn der Server beendet wird
        server_socket.close()
        print("Server gestoppt. Ports wurden geschlossen.")

def send_message_history(conn):
    try:
        with open(MESSAGE_FILE, "r") as file:
            messages = file.readlines()
            conn.sendall("".join(messages).encode())
    except:
        pass

if __name__ == "__main__":
    start_server()
