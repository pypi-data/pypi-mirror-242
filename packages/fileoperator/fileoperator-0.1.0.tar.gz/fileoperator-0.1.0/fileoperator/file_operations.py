import os
import subprocess
import sys


def open_exe(file_path):
    """
    Opens executable file for user specific OS.

    :param file_path: Path to specified file.
    """
    try:
        if sys.platform == "windows":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.run(
                ["open", file_path],
            )
        elif sys.platform == "linux":
            subprocess.run(["xdg-open", file_path])
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def close_exe(file_path):
    """
    Closes executable file for user specific OS.

    :param file_path: Path to specified file.
    """

    def close_exe_windows(file_path):
        exe_name = os.path.basename(file_path)
        try:
            subprocess.run(["taskkill", "/F", "/IM", exe_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to close {exe_name}: {e}")

    def get_app_name(file_path):
        app_map = {
            ".txt": "TextEdit",
            ".exe": "Wine",
            ".app": "Finder",
            ".png": "Preview",
            ".jpg": "Preview",
            ".pdf": "Preview",
        }
        _, file_extension = os.path.splitext(file_path)
        return app_map.get(file_extension.lower())

    def close_exe_mac(file_path):
        app_name = get_app_name(file_path)

        if app_name:
            script = f"""
            tell application "{app_name}"
                quit
            end tell
            """
        try:
            subprocess.run(["osascript", "-e", script], check=True)
        except FileNotFoundError:
            print("File not found.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to close file {app_name}: {e}")

    def close_exe_linux(file_path):
        process_name = os.path.basename(file_path)
        try:
            subprocess.run(["pkill", "-f", process_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to close {process_name}: {e}")

    try:
        if sys.platform == "windows":
            close_exe_windows(file_path)
        elif sys.platform == "darwin":
            close_exe_mac(file_path)
        elif sys.platform == "linux":
            close_exe_linux(file_path)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_file(file_path):
    """
    Reads the contents of a file.

    :param file_path: The path to the file to read.
    :return: The contents of the file.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_file(file_path, data):
    """
    Writes data to a file.

    :param file_path: The path to the file where data will be written.
    :param data: The data to write to the file.
    """
    try:
        with open(file_path, "w") as file:
            file.write(data)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_file_to_clipboard(file_path):
    """
    Copies the contents of a file to the clipboard.

    :param file_path: Path to the file whose contents are to be copied.
    """
    try:
        import pyperclip

        with open(file_path, "r") as file:
            contents = file.read()
            pyperclip.copy(contents)
            print("Contents copied to clipboard.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_file(file_path):
    """
    Creates a file.

    :param file_path: path to create file.
    """
    try:
        with open(file_path, "a") as file:
            file.write("")
    except Exception as e:
        print(f"An error occurred: {e}")


def append_data_to_file(file_path, data):
    """
    Appends data to file. Creates the file if it doesnt exist.

    :param file_path: Path to file the file to append data.
    :param data: data to append to file.
    """
    try:
        with open(file_path, "a") as file:
            file.write(data)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def move_file(input_file_path, output_file_path):
    """
    Move/rename file to specified file path

    :param input_file_path: Path to file you want to move.
    :param output_file_path: Path to move file to.
    """
    try:
        os.rename(input_file_path, output_file_path)
    except FileNotFoundError:
        print("file not found.")
    except Exception as e:
        print(f"an error occurred: {e}")


def delete_file(file_path):
    """
    deletes a file.

    :param file_path: path to delete file.
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print("file not found.")
    except Exception as e:
        print(f"an error occurred: {e}")


def make_dir(dir_path):
    """
    create a directory to specified file path.

    :param dir_path: path to create directory.
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        print(f"An error occurred while creating directory: {e}")


def delete_dir(dir_path):
    """
    delete a directory in specified path.

    :param dir_path: path to delete directory.
    """
    try:
        import shutil

        shutil.rmtree(dir_path)
    except FileNotFoundError:
        print("Directory not found.")
    except Exception as e:
        print(f"An error occurred while deleting directory: {e}")


def get_file_size(file_path):
    """
    Get size of file in specified file path.

    :param file_path: path to file.
    :return: size of file.
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def does_file_exist(file_path) -> bool:
    """
    Check if file exists in specified file path.

    :param file_path: path to file.
    :param return: boolean.
    """
    try:
        return os.path.exists(file_path)
    except FileNotFoundError:
        print("File not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def list_dir_files(dir_path):
    """
    List files in specified path.

    :param dir_path: path to directory.
    """
    try:
        return os.listdir(dir_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def change_file_perm(file_path, mode):
    """
    Change permission of a file in specified path.

    :param file_path: path to file.
    :mode: Permission type.
    """
    try:
        os.chmod(file_path, mode)
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error has occurred: {e}")


def get_file_perm(file_path):
    """
    Get permission of a file in specified path.

    :param file_path: path to file.
    :return: permission of file.
    """
    try:
        return oct(os.stat(file_path).st_mode)[-3:]
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error has occurred: {e}")
        return None


def get_file_type(file_path):
    """
    Get file type in specified path.

    :param file_path: path to file.
    :return: file type.
    """
    try:
        import mimetypes

        return mimetypes.guess_type(file_path)[0]
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_num_lines(file_path):
    """
    Get number of lines in a file in specified path.

    :param file_path: path to file.
    :return: number of lines in file.
    """
    try:
        with open(file_path, "r") as file:
            return sum(1 for line in file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_num_words(file_path):
    """
    Get number of words in a file in specified path.

    :param file_path: path to file.
    :return: number of words.
    """
    try:
        with open(file_path, "r") as file:
            return sum(len(line.split()) for line in file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_word_freq(file_path, word):
    """
    Get number of occurances of word in a file in specified path.

    :param file_path: path to file.
    :word: string
    :return: number of occurances of word.
    """
    try:
        count = 0
        with open(file_path, "r") as file:
            for line in file:
                count += line.lower().split().count(word.lower())
        return count
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_num_chars(file_path):
    """
    Get number of characters in a file in specified path.

    :param file_path: path to file.
    :return: number of characters.
    """
    try:
        with open(file_path, "r") as file:
            return sum(len(line) for line in file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_char_freq(file_path, char):
    """
    Get number of occurances of character in a file in specified path.

    :param file_path: path to file.
    :char: char
    :return: number of occurances of char.
    """
    try:
        count = 0
        with open(file_path, "r") as file:
            for line in file:
                count += line.count(char)
        return count
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def is_dir_empty(dir_path) -> bool:
    """
    check if directory is empty in specified path.

    :param dir_path: path to directory.
    :return: bool value.
    """
    try:
        return not os.listdir(dir_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def create_temp_file():
    """
    Create a temporary file in target directory.

    :return: path to temporary file.
    """
    try:
        import tempfile

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        return temp_file.name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_system_usage(path):
    """
    Get the disk usage statistics from path.

    :return: System usage information in bytes.
    """
    try:
        import shutil

        total, used, free = shutil.disk_usage(path)
        return total, used, free
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None


def monitor_file(file_path):
    """
    Monitor file for changes.

    :param file_path: Path to file.
    """
    last_modified = None
    try:
        while True:
            stat = os.stat(file_path)
            if last_modified is None or last_modified != stat.st_mtime:
                print(f"File {file_path} modified.")
                last_modified = stat.st_mtime
            return
    except FileNotFoundError:
        print("File not found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_base64(file_path):
    """
    Convert file to base64.

    :param file_path: Path to file.
    """
    try:
        import base64

        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
            return encoded_string.decode()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_symbolic_link(source_path, link_path):
    """
    Creates a symbolic link pointing to a source path.

    :param source_path: Path to the source.
    :param link_path: Path to the symbolic link.
    """
    try:
        os.symlink(source_path, link_path)
        print(f"Symbolic link created at {link_path} pointing to {source_path}")
    except OSError as e:
        print(f"An error occurred while creating symbolic link: {e}")


def split_file(file_path, number_of_parts):
    """
    Splits a file into multiple parts.

    :param file_path: Path to the file.
    :param number_of_parts: Number of parts to split the file into.
    """
    try:
        file_size = os.path.getsize(file_path)
        part_size = file_size // number_of_parts
        with open(file_path, "rb") as file:
            for i in range(number_of_parts):
                with open(f"{file_path}.part{i}", "wb") as part_file:
                    part_file.write(file.read(part_size))
    except Exception as e:
        print(f"An error occurred: {e}")


def merge_file(part_files, output_file_path):
    """
    Merges multiple file parts into a single file.

    :param part_files: List of file parts to merge.
    :param output_file_path: Path to the output file.
    """
    try:
        with open(output_file_path, "wb") as outfile:
            for part_file_path in part_files:
                with open(part_file_path, "rb") as infile:
                    outfile.write(infile.read())
    except Exception as e:
        print(f"An error occurred: {e}")


def replace_data(file_path, old_data, new_data):
    """
    Replaces specified data in a file.

    :param file_path: Path to the file.
    :param old_data: Data to be replaced.
    :param new_data: New data to replace with.
    """
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
        file_contents = file_contents.replace(old_data, new_data)
        with open(file_path, "w") as file:
            file.write(file_contents)
    except Exception as e:
        print(f"An error occurred: {e}")


def monitor_dir(directory_path):
    """
    Monitors a directory for any changes.

    :param directory_path: Path to the directory to monitor.
    :param interval: Time interval in seconds to check for changes.
    """
    last_seen = set(os.listdir(directory_path))
    try:
        while True:
            current_state = set(os.listdir(directory_path))
            if current_state != last_seen:
                print("Change detected in directory")
                last_seen = current_state
            return
    except Exception as e:
        print(f"An error occurred: {e}")


def does_dir_exist(dir_path):
    """
    Checks if a directory exists.

    :param directory_path: Path to the directory.
    :return: True if directory exists, False otherwise.
    """
    return os.path.isdir(dir_path)


def does_data_exist(file_path, data):
    """
    Checks if the given data exists in the file.

    :param file_path: Path to the file.
    :param data: Data to check for.
    :return: True if data exists, False otherwise.
    """
    try:
        with open(file_path, "r") as file:
            return data in file.read()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def compare_files(file_path1, file_path2):
    """
    Compares two files to see if they are identical.

    :param file_path1: Path to the first file.
    :param file_path2: Path to the second file.
    :return: True if files are identical, False otherwise.
    """
    import filecmp

    return filecmp.cmp(file_path1, file_path2)


def concat_files(file_paths, output_file_path):
    """
    Concatenates multiple files into one.

    :param file_paths: List of file paths to concatenate.
    :param output_file_path: Path to the output file.
    """
    try:
        with open(output_file_path, "w") as outfile:
            for file_path in file_paths:
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())
    except Exception as e:
        print(f"An error occurred: {e}")


def get_data_from_file(file_path, data):
    """
    Retrieves specific data from a file.

    :param file_path: Path to the file.
    :param data: Specific data to retrieve.
    :return: Boolean indicating if the data is found in the file.
    """
    try:
        with open(file_path, "r") as file:
            return data in file.read()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
