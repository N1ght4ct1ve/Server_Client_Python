import os
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

USERNAME_FILE = "username.txt"

def read_username():
    if os.path.exists(USERNAME_FILE):
        with open(USERNAME_FILE, "r") as file:
            username = file.read().strip()
    else:
        username = input("Gib deinen Benutzernamen ein: ")
        with open(USERNAME_FILE, "w") as file:
            file.write(username)
    return username

def receive_messages(client_socket, chat_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            chat_area.insert(tk.END, message + "\n")
        except:
            break

def send_message(event=None):
    message = input_entry.get()
    chat_area.insert(tk.END, f"[{username}]: {message}\n")  # Nachricht im Chatfenster anzeigen
    client_socket.sendall(message.encode())
    input_entry.delete(0, tk.END)

def start_client():
    global client_socket, input_entry, chat_area, username

    host = "10.10.10.199"  # Server-IP-Adresse
    port = 12345           # Portnummer, auf dem der Server lauscht

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Verbunden mit dem Chat-Server auf {host}:{port}")

    # Benutzernamen vom Benutzer abfragen oder aus der Datei laden
    username = read_username()
    client_socket.sendall(username.encode())

    # GUI erstellen
    root = tk.Tk()
    root.title("Chat Client")
    root.geometry("400x400")

    # Chat-Area erstellen
    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    chat_area.pack(expand=True, fill=tk.BOTH)

    # Eingabefeld für Chat erstellen
    input_entry = tk.Entry(root)
    input_entry.pack(expand=True, fill=tk.X, side=tk.BOTTOM)
    input_entry.bind("<Return>", send_message)

    # Thread für das Empfangen von Nachrichten vom Server starten
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_area))
    receive_thread.start()

    root.mainloop()

    # Nach dem Beenden des Hauptfensters wird die Verbindung geschlossen
    client_socket.close()
    print("Verbindung zum Server beendet.")

if __name__ == "__main__":
    start_client()
