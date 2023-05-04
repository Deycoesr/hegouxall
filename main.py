import _lzma
import os
import sys
import tarfile
import py7zr
from pathlib import Path
from send2trash import send2trash

if __name__ == '__main__':
    cwd = os.getcwd()

    password = input('password: ')

    print('start')

    tar_paths = []
    for path in Path(cwd).iterdir():
        if path.is_file() and path.suffix == '.tar':
            print('extract tar file: ' + str(path))

            with tarfile.open(path) as tar_file:
                tar_file.extractall(cwd)

            tar_paths.append(path)

    for tar_path in tar_paths:
        seven_zip_path = tar_path.with_suffix('.7z')

        if seven_zip_path.exists() and seven_zip_path.is_file():
            print('extract 7z file: ' + str(seven_zip_path))

            seven_zip_file = None
            try:
                seven_zip_file = py7zr.SevenZipFile(seven_zip_path, mode='r', password=password)
                seven_zip_file.extractall(cwd)
            except _lzma.LZMAError as e:
                if e.__str__() == 'Corrupt input data':
                    print(f'incorrect password \'{password}\'')
                    input('Press Enter to exit')
                    sys.exit(1)
                else:
                    raise e
            finally:
                if seven_zip_file is not None:
                    seven_zip_file.close()

            print('move to trash: ' + str(seven_zip_path))
            send2trash(seven_zip_path)

            print('move to trash: ' + str(tar_path))
            send2trash(tar_path)

    print('done')
    input('Press Enter to exit')
