import os
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import datetime

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

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("[Server]: Aktive Benutzer:"):
                update_user_list(message.splitlines()[1:])  # Benutzerliste aktualisieren
            else:
                chat_area.configure(state=tk.NORMAL)  # Enable the chat_area for editing
                chat_area.insert(tk.END, message + "\n")
                chat_area.configure(state=tk.DISABLED)  # Disable the chat_area after updating
        except:
            break

def update_user_list(users):
    user_list.delete(0, tk.END)  # Vorherige Liste löschen
    for user in users:
        user_list.insert(tk.END, user)

def send_message(event=None):
    message = input_entry.get()
    chat_area.configure(state=tk.NORMAL)  # Enable the chat_area for editing

    # Get the current timestamp (hour:minute)
    current_time = datetime.datetime.now().strftime("%H:%M")
    formatted_message = f"[{current_time}] [{username}]: {message}"

    chat_area.insert(tk.END, formatted_message + "\n")  # Nachricht im Chatfenster anzeigen
    chat_area.configure(state=tk.DISABLED)  # Disable the chat_area after updating
    client_socket.sendall(message.encode())
    input_entry.delete(0, tk.END)

def start_client():
    global client_socket, input_entry, chat_area, username, user_list

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
    root.geometry("400x500")  # Höhe erhöht, um Platz für die Benutzerliste zu schaffen

    # Chat-Area erstellen
    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12))
    chat_area.pack(expand=True, fill=tk.BOTH)

    # Eingabefeld für Chat erstellen
    input_entry = tk.Entry(root, font=("Helvetica", 12))
    input_entry.pack(expand=True, fill=tk.X, side=tk.BOTTOM)
    input_entry.bind("<Return>", send_message)

    # Benutzerliste erstellen
    user_list_label = tk.Label(root, text="Benutzerliste:", font=("Helvetica", 12, "bold"))
    user_list_label.pack(anchor=tk.W, padx=10, pady=(5, 0))

    user_list = tk.Listbox(root, font=("Helvetica", 12), selectbackground="#f2f2f2", selectforeground="black")
    user_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    # Thread für das Empfangen von Nachrichten vom Server starten
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    root.mainloop()

    # Nach dem Beenden des Hauptfensters wird die Verbindung geschlossen
    client_socket.close()
    print("Verbindung zum Server beendet.")

if __name__ == "__main__":
    start_client()
