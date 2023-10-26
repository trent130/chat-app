# common.py

def format_message(sender, message):
    """
    Formats a chat message with the sender's name.
    
    Args:
        sender (str): The sender's username.
        message (str): The message content.

    Returns:
        str: The formatted message.
    """
    return f"{sender}: {message}"

def parse_message(message):
    """
    Parses a formatted chat message to extract sender and message content.

    Args:
        message (str): The formatted message.

    Returns:
        tuple: A tuple containing sender (str) and message content (str).
    """
    parts = message.split(": ", 1)
    if len(parts) == 2:
        sender, message = parts
        return sender, message
    else:
        return None, message

def send_message(socket, sender, message, encryption_function):
    """
    Sends a formatted and optionally encrypted message over a socket.

    Args:
        socket: The socket object used for communication.
        sender (str): The sender's username.
        message (str): The message content.
        encryption_function: A function for encrypting the message (can be None for plaintext).
    """
    formatted_message = format_message(sender, message)
    if encryption_function:
        encrypted_message = encryption_function(formatted_message)
        socket.send(encrypted_message)
    else:
        socket.send(formatted_message.encode())

def receive_message(socket, decryption_function):
    """
    Receives a message from a socket and optionally decrypts it.

    Args:
        socket: The socket object used for communication.
        decryption_function: A function for decrypting the message (can be None for plaintext).

    Returns:
        str: The received message content.
    """
    message = socket.recv(1024)
    if decryption_function:
        return decryption_function(message)
    else:
        return message.decode()
