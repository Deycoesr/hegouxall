import _lzma
from dataclasses import dataclass
import locale
import os
import sys
import tarfile
import py7zr
from pathlib import Path
from send2trash import send2trash


@dataclass
class MessageSource:
    start: str
    extract_tar: str
    move_to_trash: str
    extract_7z: str
    incorrect_password: str
    done: str
    press_enter_to_exit: str
    input_password: str


message_sources = {
    'en': MessageSource(
        'start', 'extract tar file: {}', 'move to trash: {}', 'extract 7z file: {}', 'incorrect password \'{}\'',
        'done', 'Press Enter to exit...', 'password: '
    ),
    'zh': MessageSource(
        '开始', '解压 tar 文件: {}', '移动到回收站: {}', '解压 7z 文件: {}', '错误的密码 \'{}\'',
        '完成', '按回车键退出程序...', '密码: '
    )
}


def determine_message_source(default_region='en'):
    try:
        region_code = locale.getdefaultlocale()[0]
        region = region_code[0:region_code.index('_')]
        __message_source = message_sources.get(region)
        if __message_source is not None:
            return __message_source
    except ValueError:
        print('use default region: ' + default_region)

    return message_sources.get(default_region)


if __name__ == '__main__':
    message_source = determine_message_source()
    cwd = os.getcwd()

    print(message_source.start)

    for path in Path(cwd).iterdir():
        if path.is_file() and path.suffix == '.tar':
            print(message_source.extract_tar.format(str(path)))

            with tarfile.open(path) as tar_file:
                tar_file.extractall(cwd)

            print(message_source.move_to_trash.format(str(path)))
            send2trash(path)

    password = None

    for path in Path(cwd).iterdir():
        if path.is_file() and path.suffix == '.7z':
            if password is None:
                password = input('\n' + message_source.input_password)

            print(message_source.extract_7z.format(str(path)))

            seven_zip_file = None
            try:
                seven_zip_file = py7zr.SevenZipFile(path, mode='r', password=password)
                seven_zip_file.extractall(cwd)
            except _lzma.LZMAError as e:
                if e.__str__() == 'Corrupt input data':
                    print(message_source.incorrect_password.format(password))
                    input(message_source.press_enter_to_exit)
                    sys.exit(1)
                else:
                    raise e
            finally:
                if seven_zip_file is not None:
                    seven_zip_file.close()

            print(message_source.move_to_trash.format(str(path)))
            send2trash(path)

    print(message_source.done)
    input(message_source.press_enter_to_exit)
