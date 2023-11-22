import zipfile
import os
import sys


def unzip_lib():
    from tkinteri.core import local
    zip_file = zipfile.ZipFile(os.path.join(local, "lib.zip"))   # 652kb
    zip_file.extractall(
        os.path.join(
            os.path.dirname(sys.executable),
            "tcl"
        )  # 设置库安装地址
    )
    zip_file.close()


if __name__ == '__main__':
    unzip_lib()