"""
import fileoperator

print(fileoperator.get_key())  # b'sIkLV9riW9fEm4n4QM-uhBKaGoJ5lI-eWofBJtlFkOE='

fileoperator.encrypt_file(
    "testdir/test.txt",
   "testdir/testencrypt.txt",
    b"sIkLV9riW9fEm4n4QM-uhBKaGoJ5lI-eWofBJtlFkOE=",
)

fileoperator.decrypt_file(
    "testdir/testencrypt.txt",
    "testdir/testdecrypt.txt",
    b"sIkLV9riW9fEm4n4QM-uhBKaGoJ5lI-eWofBJtlFkOE=",
)
"""
