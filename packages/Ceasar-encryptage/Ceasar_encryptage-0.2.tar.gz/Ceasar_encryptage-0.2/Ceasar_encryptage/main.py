from encrypt import EncryptionHandler

def main():
    user_password = input("Veuillez entrer le mot de passe : ")
    try:
        encryption_handler = EncryptionHandler(user_password)
    except ValueError as e:
        print(f"Erreur : {e}")
        return

    text_to_encrypt = "Hello, World!"
    encrypted_text = encryption_handler.encrypt(text_to_encrypt)
    print(f"Texte chiffré : {encrypted_text}")

    decrypted_text = encryption_handler.decrypt(encrypted_text)
    print(f"Texte déchiffré : {decrypted_text}")

if __name__ == "__main__":
    main()
