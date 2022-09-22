import re
import urllib3
import shutil
import paramiko
from ftplib import FTP
from urllib3.util import Retry
from base_downloader import BaseDownloader
from paramiko.ssh_exception import AuthenticationException, ChannelException, SSHException
from urllib3.exceptions import ConnectTimeoutError, HTTPError, MaxRetryError

class HttpDownloader(BaseDownloader):

    def __init__(self, default_dir='/tmp', retries=3):
        super(HttpDownloader, self).__init__(default_dir)
        self.retries = retries

    def download(self, uri, filename):
        try:
            with urllib3.PoolManager() as http:
                with open(filename, 'wb') as file:
                    resp = http.request('GET', uri, preload_content=False, retries=Retry(self.retries))
                    shutil.copyfileobj(resp, file)
            print("----Download successful for {0}----".format(uri))
            print("----File saved at {0}----".format(filename))
        except (ConnectTimeoutError, HTTPError, MaxRetryError) as e:
            self.clean_up(e, filename)

class SFTPDownloader(BaseDownloader):

    def __init__(self, port=22, private_key=None, default_dir='/tmp'):
        super(SFTPDownloader, self).__init__(default_dir)
        self.private_key = private_key
        self.port = port

    def _extract_credentials(self, uri):
        # If there is no @ sign, no user/pw are given
        if not '@' in uri:
            return None, None
        # Otherwise, extract per below
        # sftp://user:password@example.com:/test/file -> user, password
        creds = uri.split("//")[1].split("@")[0]
        if creds:
            user, password = creds.split(":")
            return user, password
        return None, None

    def _extract_hostname(self, uri):
        # sftp://user:password@example.com:/test/file -> example.com
        if not "@" in uri:
            cleaned_uri = uri.split("//")[1]
            hostname = cleaned_uri.split(":")[0]
        else:
            hostname = uri.split("@")[1].split(":")[0]
        return hostname

    def _extract_remote_path(self, uri):
        # sftp://user:password@example.com:/test/file -> /test/file
        return uri.split(":")[-1]

    def generate_filename(self, uri):
        # Sometimes we don't get username:password@hostname, so need to split by //
        if not "@" in uri:
            cleaned_uri = uri.split("//")[1]
        else:
            cleaned_uri = uri.split("@")[1]
        filename = re.sub(r"(\/|:)", "-", cleaned_uri)
        filename = re.sub(r"(-)\1+", "\1", filename) # remove annoying '--' in filename
        return "{0}/{1}".format(self.default_dir, filename)

    def download(self, uri, filename):

        # Extract conn. info from URI
        user, password = self._extract_credentials(uri)
        host = self._extract_hostname(uri)
        remote_path = self._extract_remote_path(uri)

        # Prepare transport and get file
        try:
            # Init connection variables
            sftp, transport = None, None
            transport = paramiko.Transport((host, self.port))
            
            if user and password:
                transport.connect(username=user, password=password)
            elif self.private_key:
                transport.connect(pkey=self.private_key)

            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remote_path, filename)

            print("----Download successful for {0}----".format(uri))
            print("----File saved at {0}----".format(filename))
        except (AuthenticationException, ChannelException, SSHException) as e:
            self.clean_up(e, filename)
        finally: # Ensure all connections are closed
            if sftp:
                sftp.close()
            if transport:
                transport.close()

class FTPDownloader(SFTPDownloader):
    
    def __init__(self, default_dir='/tmp'):
        super(FTPDownloader, self).__init__(default_dir)
    
    def download(self, uri, filename):
        
        # Extract conn. info from URI
        # Use all extract methods from parent class
        user, password = self._extract_credentials(uri)
        host = self._extract_hostname(uri)
        remote_path = self._extract_remote_path(uri)

        # Init FTP
        ftp = FTP(host)
        try:
            if user and password:
                ftp.login(user, password)
            else:
                ftp.login()

            with open(filename, 'wb') as fp:
                ftp.retrbinary('RETR {0}'.format(remote_path), fp.write)
            print("----Download successful for {0}----".format(uri))
            print("----File saved at {0}----".format(filename))
        except Exception as e:
            self.clean_up(e, filename)
        finally: # Ensure all connections are closed
            ftp.close()


