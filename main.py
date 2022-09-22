import argparse
from config import DOWNLOADERS, DEFAULT_DIR
from utils import extract_protocol

parser = argparse.ArgumentParser(description='Utility tool for downloading files')
parser.add_argument("--uri")
args = parser.parse_args()
uri = args.uri

def main():
    protocol = extract_protocol(uri)
    downloader = DOWNLOADERS.get(protocol)

    if downloader:
        print("Using {0} to download".format(downloader.__name__))
        executor = downloader(default_dir=DEFAULT_DIR)
        executor.run(uri)
    else:
        print("Given protocol is not supported: {0}".format(protocol))

if __name__ == '__main__':
    main()    
