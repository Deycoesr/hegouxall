import _lzma
import os
import sys
import tarfile
import py7zr
from pathlib import Path
from send2trash import send2trash

if __name__ == '__main__':
    cwd = os.getcwd()

    print('start')

    for path in Path(cwd).iterdir():
        if path.is_file() and path.suffix == '.tar':
            print('extract tar file: ' + str(path))

            with tarfile.open(path) as tar_file:
                tar_file.extractall(cwd)

            print('move to trash: ' + str(path))
            send2trash(path)

    password = input('\n\npassword: ')

    for path in Path(cwd).iterdir():
        if path.is_file() and path.suffix == '.7z':
            print('extract 7z file: ' + str(path))

            seven_zip_file = None
            try:
                seven_zip_file = py7zr.SevenZipFile(path, mode='r', password=password)
                seven_zip_file.extractall(cwd)
            except _lzma.LZMAError as e:
                if e.__str__() == 'Corrupt input data':
                    print(f'incorrect password \'{password}\'')
                    input('Press Enter to exit...')
                    sys.exit(1)
                else:
                    raise e
            finally:
                if seven_zip_file is not None:
                    seven_zip_file.close()

            print('move to trash: ' + str(path))
            send2trash(path)

    print('done')
    input('Press Enter to exit...')
