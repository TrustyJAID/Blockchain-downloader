# Blockchain-downloader

Downloads information from the blockchain.

This code has been modified from several sources and is free to use.

Code used is modified versions of `jean.py` to download data from blockchain.info as well as the satoshi downloader script.

## Instructions

- Install Python 2.7 and `pip`
    - Windows: https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
    - Linux: `$ sudo apt-get install python-pip`
- During install when it asks for what modules to install, ensure that the last option "install to `PATH`" is enabled.
- After installing, run Command Prompt/Terminal
- Change directory to where the file is saved (`cd /path/to/folder`)
- Install the requirements with `pip`
    - `pip install -r requirements.txt`
- Run the command: `python blockchain_downloader.py [TRANSACTION_ID] [OUTPUT_FILENAME]`
    - `TRANSACTION_ID` is optional (don't include the `[]` brackets).  It will ask for one upon start if one isn't supplied.
    - `OUTPUT_FILENAME` is optional (don't include the `[]` brackets).  The default output filename is 'file'.
- If you have the bitcoin RPC service setup with a local blockchain, add it to the rpclogin.txt file.
    -username in the first line and password in the second line.
- enable RPC by adding bitcoin.conf to the folder with the blocks folder Appdata on windows default
    -https://github.com/bitcoin/bitcoin/blob/master/contrib/debian/examples/bitcoin.conf
    -Add txindex=1 
    -enable rpcport:8332 
    -change rpcuser and rpcpass to match rpclogin.txt
    -Add server=1

## How-to
- Run this tool inside Terminal, navigate to the download folder (cd)
- Run with "python blockchain-downloader.py <txid> <filename>" is the traditional usage
- or Run with "python blockchain-downloader.py <startblock> <endblock>" for block ranges (note: that is index height)
- inside dlfn.py under get_data_local() are self.save_file() functions used to save various versions of information:
    - You may have to remove the "# " before these functions to download the data
    - indata is the input script data
    - inhex is the input data as hex
    - hexdata is the output data as hex
    - data is the output data following the satoshi length + checksum
    - origdata is the original unmodified output data
    
