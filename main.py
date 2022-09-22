import argparse
from config import DOWNLOADERS, DEFAULT_DIR, DEFAULT_RETRY
from utils import extract_protocol

parser = argparse.ArgumentParser(description='Utility tool for downloading files')
parser.add_argument("--uri")
args = parser.parse_args()
uri = args.uri
otherArgs = {} # we may pass in args other than URI in the future

def main():
    protocol = extract_protocol(uri)
    downloader = DOWNLOADERS.get(protocol)

    if downloader:
        print("Using {0} to download".format(downloader))
        executor = downloader(default_dir=DEFAULT_DIR)
        executor.run(uri, otherArgs)
    else:
        print("Given protocol is not supported: {0}".format(protocol))

if __name__ == '__main__':
    main()    
