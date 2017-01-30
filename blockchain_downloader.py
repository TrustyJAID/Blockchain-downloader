#!/usr/bin/env python3

from __future__ import print_function
from wlffbd.blockchaininfo import get_tx_from_online
from wlffbd.blockchainrpc import make_server
from wlffbd.dlfn import dlfn
from wlffbd.filesystem import write, newline

import json
import sys
import time
try:
    # Python 3
    import urllib.request, urllib.parse, urllib.error
    import urllib.request, urllib.error, urllib.parse
    import collections
except:
    # Python 2
    import urllib
    import urllib2

try:
    import jsonrpclib
except ImportError:
    print('Fatal: jsonrpclib-pelix missing (Try `pip install -r requirements.txt`)')
    sys.exit(-1)

RPCUSER, RPCPASS = open('rpclogin.txt', 'r').read().split()
SERVER = make_server(RPCUSER, RPCPASS)
BLOCKCHAINADDRESS = ''
global FILENAME
FILENAME = 'file'       # global default filename setting
INDIVIDUALFILE = False  # Single flag for single file fore each transaction
try:
    # Checks for an RPC connection to local blockchain
    SERVER.getinfo()
    LOCAL = True
except Exception as e:
    print("RPC connection not available")
    LOCAL = False


class __main__():
    """
    Start of the main program
    This could theoretically all be made in a GUI
    """
    dlfn = dlfn(SERVER)
    if len(sys.argv) == 3:
        # This checks if two arguments were given and
        # utilises them as the transaction then the filename to save
        try:
            BLOCKCHAINADDRESS = str(sys.argv[1])
            FILENAME = str(sys.argv[2])
        except IndexError:
            print("No address or filename")

    elif len(sys.argv) == 2:
        # This checks if one argument was given
        # and uses it as the transaction and default file name
        try:
            BLOCKCHAINADDRESS = str(sys.argv[1])
            FILENAME = 'File'
        except IndexError:
            print("no address")

    elif len(sys.argv) == 1:
        # This works if no arguments are given to allow the program to function
        BLOCKCHAINADDRESS = input('Enter the blockchain Address or transactions file:')
        FILENAME = input('Enter the file name you would like to save to:')
        if FILENAME == '':
            # This gives a default filename
            FILENAME = 'file.txt'

    if BLOCKCHAINADDRESS.endswith(".txt"):
        # This checks if you're giving a list of transactions or just one
        dlfn.get_tx_list(BLOCKCHAINADDRESS, LOCAL)

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
