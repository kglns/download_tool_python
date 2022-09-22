class BaseDownloader:

    def __init__(self, uris=[]):
        self.uris = uris

    def generate_filename(self, uri):
        raise 'Not implemented'

    def clean_up(self, error, filename):
        raise 'Not implemented'

    def download(self):
        raise 'Not implemented'

    def run(self):
        for uri in self.uris:
            try:
                filename = self.generate_filename(uri)
                self.download()
            except Exception as e:
                self.clean_up(e, filename)

        

    

