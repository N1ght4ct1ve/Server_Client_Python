import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            break

def start_client():
    host = "10.10.10.199"  # Server-IP-Adresse
    port = 12347           # Portnummer, auf dem der Server lauscht

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Verbunden mit dem Chat-Server auf {host}:{port}")

    # Benutzernamen vom Benutzer abfragen
    username = input("Gib deinen Benutzernamen ein: ")
    client_socket.sendall(username.encode())

    # Thread für das Empfangen von Nachrichten vom Server starten
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Nachrichten senden
    while True:
        message = input("["+username+"]:")
        if message.lower() == "exit":
            break
        client_socket.sendall(message.encode())

    client_socket.close()
    print("Verbindung zum Server beendet.")

if __name__ == "__main__":
    start_client()
