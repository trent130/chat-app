import socket
import threading
from cryptography.fernet import Fernet
import bcrypt
import sqlite3
import json
from user_management import register_user, authenticate_user


# Load server configuration from config.json
with open("config.json", "r") as config_file:
    server_config = json.load(config_file)

server_ip = server_config["server_ip"]
server_port = server_config["server_port"]
max_clients = server_config["max_clients"]
message_history_file = server_config["message_history_file"]

# Now you can use these settings in your server code


# Server configuration
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen(5)

# Connect to a SQLite database to store user credentials
conn = sqlite3.connect("user_db.db")
cursor = conn.cursor()

# Create a table to store user data (if it doesn't exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')

# Function to register a new user
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Function to authenticate a user
def authenticate_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row and bcrypt.checkpw(password.encode(), row[0]):
        return True
    return False

# List to store connected clients
clients = []

# Generate a key pair for each client
def generate_key_pair():
    private_key = Fernet.generate_key()
    public_key = Fernet.generate_key()
    return private_key, public_key

# Function to encrypt a message
def encrypt_message(message, private_key, public_key):
    shared_key = Fernet(public_key).encrypt(private_key)
    encrypted_message = Fernet(shared_key).encrypt(message.encode())
    return encrypted_message

# Function to decrypt a message
def decrypt_message(encrypted_message, private_key, public_key):
    shared_key = Fernet(public_key).encrypt(private_key)
    decrypted_message = Fernet(shared_key).decrypt(encrypted_message).decode()
    return decrypted_message

# Function to broadcast encrypted messages
def broadcast(encrypted_message, sender_socket, sender_username):
    for client in clients:
        if client[0] != sender_socket:
            try:
                decrypted_message = decrypt_message(encrypted_message, client[2], client[3])
                message = f"{sender_username}: {decrypted_message}"
                client[0].send(encrypt_message(message, client[2], client[3]))
            except:
                # Handle disconnections
                clients.remove(client)

# Function to handle client connections
def handle_client(client_socket):
    client_socket.send("Enter your username: ".encode())
    username = client_socket.recv(1024).decode()
    if authenticate_user(username, "password123"):  # Replace with user authentication logic
        client_socket.send("Connected to the chat. You can start chatting securely.".encode())
        private_key, public_key = generate_key_pair()
        client_socket.send(public_key)
        clients.append((client_socket, username, private_key, public_key))
        for c in clients:
            if c[0] != client_socket:
                c[0].send(f"{username} has joined the chat.".encode())

        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                broadcast(encrypted_message, client_socket, username)
            except:
                # Handle disconnections
                clients.remove((client_socket, username, private_key, public_key))
                for c in clients:
                    c[0].send(f"{username} has left the chat.".encode())
                break
    else:
        client_socket.send("Authentication failed. Goodbye.".encode())
        client_socket.close()

# Main server loop
while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
