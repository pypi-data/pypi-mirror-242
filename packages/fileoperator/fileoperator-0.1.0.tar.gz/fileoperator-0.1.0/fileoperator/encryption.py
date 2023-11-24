from cryptography.fernet import Fernet


def get_key():
    try:
        key = Fernet.generate_key()
        return key
    except Exception as e:
        print(f"An error occurred: {e}")


def encrypt_file(input_file_path, output_file_path, key):
    try:
        fernet = Fernet(key)
        with open(input_file_path, "rb") as file_in, open(
            output_file_path, "wb"
        ) as file_out:
            encrypted_data = fernet.encrypt(file_in.read())
            file_out.write(encrypted_data)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def decrypt_file(input_file_path, output_file_path, key):
    try:
        fernet = Fernet(key)
        with open(input_file_path, "rb") as file_in, open(
            output_file_path, "wb"
        ) as file_out:
            decrypted_data = fernet.decrypt(file_in.read())
            file_out.write(decrypted_data)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
