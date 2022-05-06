"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
"""


import PyInstaller.__main__


PyInstaller.__main__.run([
    "src/main.py",
    "--additional-hooks-dir=misc",
    "--hidden-import=sklearn.neighbors._partition_nodes",
    "--hidden-import=sklearn.utils._typedefs",
    "--icon=icon/icon.ico",
    "--paths=src",
    "--windowed"
])
