from cryptography.fernet import Fernet

def generate_key_pair():
    """
    Generates a key pair for message encryption.

    Returns:
        tuple: A pair of private key and public key.
    """
    private_key = Fernet.generate_key()
    public_key = Fernet.generate_key()
    return private_key, public_key

def encrypt_message(message, private_key, public_key):
    """
    Encrypts a message using a shared key.

    Args:
        message (str): The message to encrypt.
        private_key (bytes): The sender's private key.
        public_key (bytes): The recipient's public key.

    Returns:
        bytes: The encrypted message.
    """
    shared_key = Fernet(public_key).encrypt(private_key)
    encrypted_message = Fernet(shared_key).encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, private_key, public_key):
    """
    Decrypts an encrypted message using a shared key.

    Args:
        encrypted_message (bytes): The encrypted message.
        private_key (bytes): The recipient's private key.
        public_key (bytes): The sender's public key.

    Returns:
        str: The decrypted message.
    """
    shared_key = Fernet(public_key).encrypt(private_key)
    decrypted_message = Fernet(shared_key).decrypt(encrypted_message).decode()
    return decrypted_message
