from downloaders import HttpDownloader, SFTPDownloader

DEFAULT_DIR="/tmp"
DOWNLOADERS = {
    "http": HttpDownloader,
    "https": HttpDownloader,
    "ftp": SFTPDownloader,
    "sftp": SFTPDownloader,
}