#!/usr/bin/env python3

from __future__ import print_function
from wlffbd.blockchaininfo import get_tx_from_online
from wlffbd.blockchainrpc import make_server
from wlffbd.dlfn import dlfn
from wlffbd.filesystem import write, newline
from wlffbd.gui import Blockchain_GUI

import json
import sys
import time
import os
try:
    # Python 3
    import urllib.request, urllib.parse, urllib.error
    import urllib.request, urllib.error, urllib.parse
    import collections
    from tkinter import *
except:
    # Python 2
    import urllib
    import urllib2
    from Tkinter import *

try:
    import jsonrpclib
except ImportError:
    print('Fatal: jsonrpclib-pelix missing (Try `pip install -r requirements.txt`)')
    sys.exit(-1)

BLOCKCHAINADDRESS = ''
global FILENAME
FILENAME = 'file'       # global default filename setting
INDIVIDUALFILE = True  # Single flag for single file fore each transaction

def check_folder():
    if not os.path.exists("temp"):
        print("Creating temp folder")
        os.makedirs("temp")


if __name__ == "__main__":
    """
    Start of the main program
    This could theoretically all be made in a GUI
    """
    check_folder()
    
    if len(sys.argv) == 1:
        # Generates a GUI when no arguments are given
        root = Tk()
        bc_gui = Blockchain_GUI(root)
        root.mainloop()

    if len(sys.argv) > 1:
        # This checks if two arguments were given and
        # utilises them as the transaction then the filename to save
        try:
            BLOCKCHAINADDRESS = str(sys.argv[1])
            FILENAME = str(sys.argv[2])
        except IndexError:
            BLOCKCHAINADDRESS = str(sys.argv[1])

        RPCUSER, RPCPASS = open('rpclogin.txt', 'r').read().split()
        SERVER = make_server(RPCUSER, RPCPASS)
        try:
            # Checks for an RPC connection to local blockchain
            SERVER.getinfo()
            LOCAL = True
        except Exception as e:
            print("RPC connection not available")
            LOCAL = False
        dlfn = dlfn(SERVER)

        if BLOCKCHAINADDRESS.endswith(".txt"):
            # This checks if you're giving a list of transactions or just one
            dlfn.get_tx_list(BLOCKCHAINADDRESS, LOCAL, True)

        elif BLOCKCHAINADDRESS.isdigit() and LOCAL:
                dlfn.get_block_tx(BLOCKCHAINADDRESS, FILENAME, LOCAL)

        elif len(BLOCKCHAINADDRESS) < 64 and BLOCKCHAINADDRESS.startswith('1'):
            # Checks if wallet on main blockchain
            print("This is a wallet ID, searching...")
            print("Fetching transactions from", BLOCKCHAINADDRESS)
            tx = get_tx_from_online(BLOCKCHAINADDRESS,
                                    callback=lambda txlist, n_tx:
                                    print("Progress (if it gets 'stuck' wait a minute or two): {} / {}"
                                          .format(len(txlist), n_tx)))
            for transaction in tx:
                write(BLOCKCHAINADDRESS + ".txt", transaction + newline(), False, "ab")
        else:
            dlfn.FILENAME = FILENAME
            dlfn.save_data(BLOCKCHAINADDRESS, LOCAL, INDIVIDUALFILE)
