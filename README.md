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
- If you have the bitcoin RPC service setup with a local blockchain, add it to the RPC settings at the top of the script.
