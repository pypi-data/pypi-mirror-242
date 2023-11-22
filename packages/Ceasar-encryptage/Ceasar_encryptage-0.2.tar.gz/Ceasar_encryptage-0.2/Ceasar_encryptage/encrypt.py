from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode

class EncryptionHandler:
    def __init__(self, password):
        if password != "mon_password_secret":
            raise ValueError("Mot de passe incorrect.")
        self.key = self.generate_key(password)

    @staticmethod
    def generate_key(password):
        return Fernet.generate_key()

    def encrypt(self, text):
        fernet = Fernet(self.key)
        encrypted_text = fernet.encrypt(text.encode())
        return urlsafe_b64encode(encrypted_text)

    def decrypt(self, encrypted_text):
         fernet = Fernet(self.key)
         decrypted_text = fernet.decrypt(urlsafe_b64decode(encrypted_text)).decode('utf-8')
         return decrypted_text
