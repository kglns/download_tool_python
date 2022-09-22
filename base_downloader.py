import re
import os

class BaseDownloader:

    def __init__(self, default_dir='/tmp'):
        self.default_dir = default_dir

    ''' 
    Process URI of form ${protocol}://uri/filename into uri-filename.
    This will be common across most of the child classes, hence implemented here.
    This can be overwritten in child class as well.
    '''
    def generate_filename(self, uri):
        
        cleaned_uri = uri.split("//")[1]
        filename = re.sub(r"\/", "-", cleaned_uri)

        return "{0}/{1}".format(self.default_dir, filename)

    '''
    Prints any error during download, and remove file if exists
    '''
    def clean_up(self, error, filename):
        print("----Error occoured during downloading----")
        print(error)

        if os.path.isfile(filename):
            print("Removing file: {0}".format(filename))
            os.remove(filename)

    '''
    This method must be implemented by child classes
    '''
    def download(self, uri, filename):
        raise NotImplementedError

    def run(self, uri):
        try:
            filename = self.generate_filename(uri)
            self.download(uri, filename)
        # Catch any unhandled exceptions and log here. Specific exceptions can be handled in individual Downloader as well.
        except Exception as e:
            self.clean_up(e, filename)

        

    

