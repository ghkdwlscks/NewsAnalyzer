@echo off
REM Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
REM This is the batch file used for generating Windows installer.
REM NewsAnalyzer.zip includes build (PyInstaller output directory), config, data, fasttext and format directories.
mkdir "C:\Program Files\NewsAnalyzer"
bandizip x -y -o:"C:\Program Files\NewsAnalyzer" "NewsAnalyzer.zip"
mklink "%userprofile%\desktop\NewsAnalyzer.exe" "C:\Program Files\NewsAnalyzer\build\NewsAnalyzer.exe"
bitsadmin /transfer "Downloading pretrained fastText model..." "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.bin.gz" "C:\Program Files\NewsAnalyzer\fasttext\pretrained_model.bin.gz"
