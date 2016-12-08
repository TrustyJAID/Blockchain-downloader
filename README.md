# Blockchain-downloader
Downloads information from the blockchain

This code has been modified from several sources and is free to use
Code used is modified versions of jean.py to download data from blockchain.info as well as the satoshi downloader script.
Install Python 2.7
Install pip on windows
https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
Install pip on linux $ sudo apt-get install python-pip
During install when it asks for what modules to install
ensure that the last option install to PATH is enabled
After installing run Command Prompt/Terminal
Change directory to where the file is saved
Type: python blockchain_downloader.py
You can add the transaction after or it will ask
for one upon start if one isn't supplied
You can also add a filename to save it as after the transaction
The dafault filename is 'file'
If you have the bitcoin RPC service setup with a
local blockchain add it to the RPC settings at the top
