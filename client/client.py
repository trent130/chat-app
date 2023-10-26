import json
import socket
import threading
from cryptography.fernet import Fernet
import getpass
import time  # For message timestamps

# Load user settings from user_settings.json
with open("user_settings.json", "r") as user_settings_file:
    user_settings = json.load(user_settings_file)

# Retrieve settings for a specific user
user_id = "user123"
if user_id in user_settings:
    user_preferences = user_settings[user_id]
    notifications = user_preferences.get("notifications", {})
    display = user_preferences.get("display", {})
    sound_enabled = notifications.get("sound_enabled", True)
    desktop_notifications = notifications.get("desktop_notifications", True)
    theme = display.get("theme", "light")
    font_size = display.get("font_size", 14)

# Now you can use these user-specific settings within your server code


# Server configuration
server_ip = "localhost"
server_port = 12345

private_key = Fernet.generate_key()
public_key = Fernet.generate_key()

def encrypt_message(message, private_key, public_key):
    shared_key = Fernet(public_key).encrypt(private_key)
    encrypted_message = Fernet(shared_key).encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, private_key, public_key):
    shared_key = Fernet(public_key).encrypt(private_key)
    decrypted_message = Fernet(shared_key).decrypt(encrypted_message).decode()
    return decrypted_message

def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(encrypted_message, private_key, public_key)
            
            # Extract and format the timestamp
            timestamp = time.strftime("%H:%M:%S")
            
            print(f"[{timestamp}] {decrypted_message}")
        except:
            break

def private_message(client_socket, recipient):
    while True:
        try:
            message = input(f"Send a private message to {recipient}: ")
            if message.lower() == "/exit":
                break
            private_message = f"[@{recipient}]: {message}"
            encrypted_private_message = encrypt_message(private_message, private_key, public_key)
            client_socket.send(encrypted_private_message)
        except KeyboardInterrupt:
            break

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("Connected to the chat server.")

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Implement user authentication here

    client_socket.send(username.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.startswith("/private "):
            recipient = message.split()[1]
            private_message(client_socket, recipient)
        elif message.lower() == "/exit":
            break
        else:
            encrypted_message = encrypt_message(message, private_key, public_key)
            client_socket.send(encrypted_message)

except KeyboardInterrupt:
    print("Connection terminated.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    client_socket.close()
