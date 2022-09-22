import argparse
from config import DOWNLOADERS
from utils import extract_protocol

parser = argparse.ArgumentParser(description='Download files')
parser.add_argument("--uri")
args = parser.parse_args()

def main():
    protocol = extract_protocol(args.uri)
    downloader = DOWNLOADERS.get(protocol)

    if downloader:
        downloader.run(args.uri)
    else:
        print("Given protocol is not supported: {0}".format(protocol))

if __name__ == '__main__':
    main()    
