import paramiko
import unittest
from base_downloader import BaseDownloader
from downloaders import FTPDownloader, HttpDownloader, SFTPDownloader

class TestDownloaders(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.bad_uri = 'https://zipdia.com/test/file'
        self.good_uri = 'https://ftp.gnu.org/old-gnu/Manuals/binutils-2.12/html_mono/binutils.html'

        self.sftp_uri = 'ftp://user:pw@kaung.dev:/test/hello.txt'

        self.base_downloader = BaseDownloader()
        self.http = HttpDownloader()
    
        # key = paramiko.RSAKey.from_private_key_file("/path/to/secret")
        self.sftp = SFTPDownloader()

        self.ftp = FTPDownloader()

    # BaseClass tests
    def test_generate_filename(self):
        self.assertEqual(self.base_downloader.generate_filename(self.bad_uri), '/tmp/zipdia.com-test-file')

    # HTTP tests
    def test_http_download_successful(self):
        self.http.run(self.good_uri)

    def test_http_download_failed_max_retry_reached(self):
        self.http.run(self.bad_uri)

    # FTP/SFTP tests
    def test_sftp_download_get_creds(self):
        self.assertEqual(self.sftp._extract_credentials(self.sftp_uri), ('user', 'pw'))

    def test_sftp_download_get_hostname(self):
        self.assertEqual(self.sftp._extract_hostname(self.sftp_uri), 'kaung.dev')
    
    def test_sftp_download_get_remote_path(self):
        self.assertEqual(self.sftp._extract_remote_path(self.sftp_uri), '/test/hello.txt')
    
    def test_sftp_download_generate_filename(self):
        self.assertEqual(self.sftp.generate_filename(self.sftp_uri), '/tmp/kaung.devtest-hello.txt')

    def test_sftp_download_bad_auth_expected(self):
        self.sftp.run(self.sftp_uri)

    def test_ftp_download_from_debian_succeed(self):
        self.ftp.run("ftp://ftp.us.debian.org:/debian/README")

if __name__ == '__main__':
    unittest.main()