# fileoperator: Python File Operations Package

![fileops_logo](./public/fileops_logo.png)

## About

`fileoperator` is an all-in-one Python utility package designed to simplify and streamline a wide range of file operations. This package offers comprehensive solutions for file handling, including encryption, compression, file manipulation, and much more. Whether you're dealing with legacy code or need an efficient way to handle complex file operations, `fileops` is your go-to library.

## Features

- **File Encryption & Decryption**: Secure your files with state-of-the-art encryption standards.
- **File Compression & Decompression**: Efficiently compress and decompress files using various algorithms.
- **Data Import/Export Utilities**: Streamline the process of importing and exporting data.
- **Advanced File Manipulation**: Perform advanced file operations like batch renaming, searching, and splitting.
- **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux.

## Installation

To install fileoperator, simply run the following command in your terminal:
`pip install fileops` 

## Usage

Here are some basic examples of how `fileoperator` can be used:

### Encrypting a File
```Python
from fileoperator import encrypt_file

encrypt_file('path/to/your/file.txt', 'path/to/target/file.txt', 'your-encryption-key')
```
### Compression
```Python
from fileoperator import compress_file

compress_file('path/to/your/file.txt','path/to/compressed/file.zip')
```
## Contributing
Contributions to fileoperator are welcome! If you have a suggestion or improvement, feel free to fork the repository and submit a pull request. Check Contributing.md for more details.

## License
fileoperator is licensed under the MIT License. Check LICENSE.txt for more details.
