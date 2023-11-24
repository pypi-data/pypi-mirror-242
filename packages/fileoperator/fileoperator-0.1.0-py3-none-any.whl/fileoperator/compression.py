import zipfile
import os


def compress_file(input_file_path, output_file_path):
    try:
        with zipfile.ZipFile(output_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(input_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def decompress_file(input_file_path, output_dir_path):
    try:
        with zipfile.ZipFile(input_file_path, "r") as zipf:
            zipf.extractall(output_dir_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def compress_folder(folder_path, output_zip_path):
    """
    Compresses a folder into a zip file.

    :param folder_path: Path to the folder.
    :param output_zip_path: Path to the compressed output file.
    """
    try:
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file), os.path.join(folder_path, "..")
                        ),
                    )
    except Exception as e:
        print(f"An error occurred: {e}")


def decompress_folder(zip_file_path, output_folder_path):
    """
    Decompresses a zip file into a folder.

    :param zip_file_path: Path to the zip file.
    :param output_folder_path: Path to extract the contents to.
    """
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(output_folder_path)
    except Exception as e:
        print(f"An error occurred: {e}")
