from functools import partial
from downloaders import HttpDownloader, SFTPDownloader, FTPDownloader

DEFAULT_DIR="/tmp"
DEFAULT_RETRY=3
DOWNLOADERS = {
    "http": partial(HttpDownloader, retries=DEFAULT_RETRY),
    "https": partial(HttpDownloader, retries=DEFAULT_RETRY),
    "ftp": FTPDownloader,
    "sftp": SFTPDownloader
}