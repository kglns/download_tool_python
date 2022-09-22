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

    def remove_file(self, filename):
        if os.path.isfile(filename):
            print("Removing file: {0}".format(filename))
            os.remove(filename)
    '''
    Prints any error during download, and remove file if exists
    '''
    def clean_up(self, error, filename):
        print("----Error occoured during downloading----")
        print(error)

        self.remove_file(filename)

    '''
    This method must be implemented by child classes. Other key, value params can be added as needed.
    '''
    def download(self, uri, filename, **kwargs):
        raise NotImplementedError

    '''
    This takes care of the actual run - it also handles any uncaught exceptions and cleans up.
    '''
    def run(self, uri, **kwargs):
        try:
            filename = self.generate_filename(uri)
            self.remove_file(filename) # if a file already exits, remove it
            self.download(uri, filename, **kwargs)
        # Catch any unhandled exceptions and log here. Specific exceptions can be handled in individual Downloader as well.
        except Exception as e:
            self.clean_up(e, filename)

        

    

