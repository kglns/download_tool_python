## Usage

1. Download single URI with specified protocol.
python3 main.py --uri https://example.com/testfile

2. Multiple URIs. You can define in a config file and pass in the file as param. See test_uris.txt for example.
./parallel_download.sh test_uris.txt

3. Parallel download. Same as 2. It runs all uris provided in cfg in parallel.

4. To configure download location / number of retries, edit config.py

## Architecture

This tool has 4 components.

1. base_downloader.py
`
It has a BaseDownloader class which can be inherited. The class handles common actions such as generating file name, and handling uncaught exceptions.
download must be implemented
`

2. config.py
`
It encapsulates default params such as download location, retries, etc.
To add a new protocol, write a new class in downloaders.py and register in DOWNLOADERS dictionary.
`

3. downloaders.py
`
It hosts all implementations of downloaders with specific protocols.
`


4. main.py
`
It picks up cmd args and routes to correct downloader instance.
`