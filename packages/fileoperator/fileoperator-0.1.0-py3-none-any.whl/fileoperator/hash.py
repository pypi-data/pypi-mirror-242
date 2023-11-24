def get_hash(file_path, hash_algo="sha256"):
    """
    Computes hash of a file using the specified hash algorithm

    :param file_path: Path to file.
    :param hash_algo: Hash algorithm (default: sha256)
    :param return: hash of file.
    """
    try:
        import hashlib

        hash = hashlib.new(hash_algo)
        with open(file_path, "rb") as file:
            read = file.read()
            hash.update(read)
        return hash.hexdigest()
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"An error occurred during hashing: {e}")
        return None


def verify_file_checksum(file_path, expected_checksum, hash_algo="sha256"):
    """
    Verifies the checksum of a file.

    :param file_path: Path to the file.
    :param expected_checksum: Expected checksum value.
    :param hash_algo: Hash algorithm used for checksum (default: 'sha256').
    """
    import hashlib

    hasher = hashlib.new(hash_algo)
    try:
        with open(file_path, "rb") as file:
            buf = file.read()
            hasher.update(buf)
        file_checksum = hasher.hexdigest()
        return file_checksum == expected_checksum
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
