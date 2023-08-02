import socket
import threading

def handle_client_connection(conn, addr, clients):
    print(f"Verbunden mit: {addr[0]}:{addr[1]}")
    username = conn.recv(1024).decode()
    clients[conn] = username

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"{clients[conn]}: {message}")
            # Weiterleiten der Nachricht an alle anderen verbundenen Clients
            for client, name in clients.items():
                if client != conn:
                    client.sendall(f"[{clients[conn]}]: {message}".encode())
    except:
        pass

    print(f"Verbindung zu {addr[0]}:{addr[1]} geschlossen.")
    del clients[conn]
    conn.close()

def start_server():
    host = "0.0.0.0"  # Server lauscht auf allen verfügbaren IP-Adressen
    port = 12345    # Portnummer, auf dem der Server lauscht

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Chat-Server gestartet. Warte auf Verbindungen auf {host}:{port}")

    connected_clients = {}  # Wörterbuch zum Speichern der verbundenen Clients und Benutzernamen

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr, connected_clients))
            client_thread.start()
    except KeyboardInterrupt:
        # Bei einem Tastenabbruch (z. B. durch CTRL+C) den Server beenden
        pass
    finally:
        # Socket schließen, wenn der Server beendet wird
        server_socket.close()
        print("Server gestoppt. Ports wurden geschlossen.")

if __name__ == "__main__":
    start_server()
