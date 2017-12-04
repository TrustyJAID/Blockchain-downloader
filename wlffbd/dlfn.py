# -*- coding: utf-8 -*-
'''dlfn class and methods'''

from __future__ import print_function
from . import satoshi
from . import blockchaininfo as online
from . import blockchainrpc as rpc
from .filesystem import read, readlines, write, newline
from .search import search_hex, check_hash, search_words, get_extension

from timeit import default_timer as timer

import struct

# RPCUSER, RPCPASS = read('rpclogin.txt', 'r').split()
# SERVER = rpc.make_server(RPCUSER, RPCPASS)

class dlfn():
    # FILENAME = ''
    # RPCUSER, RPCPASS = read('rpclogin.txt', 'r').split()
    # SERVER = rpc.make_server(RPCUSER, RPCPASS)

    def __init__(self, SERVER, FILENAME='file'):
        self.FILENAME = FILENAME
        self.SERVER = SERVER

    def save_data(self, transaction, LOCAL=False, single_file=True):
        if LOCAL:
            hexdata = rpc.get_data_local(transaction, self.SERVER)
            inhex = rpc.get_indata_local(transaction, self.SERVER)
        else:
            page = online.get_blockchain_transaction_json(transaction)
            hexdata = online.get_data_online(page)
            inhex = online.get_indata_online(page)
        indata = satoshi.unhexutf8(inhex)
        origdata = satoshi.unhexutf8(hexdata)
        # print(hexdata[-700:] + "\n\n\n" + hexdata2[-700:])
        _, _, data = satoshi.length_checksum_data_from_rawdata(origdata)
        significanttx = ''
        significanttx += search_hex(hexdata, " output")
        significanttx += search_hex(inhex, " input")
        # significanttx += check_hash(inhex+hexdata, 'ripemd160')
        if self.checksum(origdata):
            significanttx += " Satoshi Checksum found"
        if search_words(origdata):
            significanttx += " ASCII letters found output"
            # print(origdata)
        if search_words(indata):
            significanttx += " ASCII letters found input"
        if single_file:
            extension = get_extension(significanttx)
        if not single_file:
            extension = "txt"
        if significanttx != '':
            print(transaction + " " + significanttx)
            write("significant.txt", transaction + " " + significanttx + newline(),  False, 'ab')
        if "Satoshi" in significanttx:
            write("temp/" + self.FILENAME+"data." + extension, data, True, 'ab')
        write("temp/" + self.FILENAME+"indata." + extension, indata, True, 'ab')     # saves the input script
        write("temp/" + self.FILENAME+"origdata." + extension, origdata, True, 'ab')         # saves all binary data

    def get_tx_list(self, tx_list, LOCAL, single_file):
        """This function checks the blockchain for all transactions in the FILENAME document """
        for line in readlines(tx_list):
            blockhash = line.rstrip('\r\n')
            if blockhash:
                self.save_data(blockhash, LOCAL, single_file)

    def get_block_tx(self, start, end, LOCAL):
        """This function checks the blockchain for all transactions in the FILENAME document """
        if not end.isdigit():
            end = rpc.get_block_height(self.SERVER)
        for i in range(int(start), int(end)):
            start = timer()
            hashlist = rpc.get_block_transactions(i, self.SERVER)
            for tx in hashlist:
                self.save_data(tx, LOCAL)
            endtime = timer() - start
            print("Block number: {0} | Time to complete:{1:.2f}s | Number of transactions: {2}"
                  .format(i, endtime, len(hashlist)))

    def checksum(self, data):
        """
        verify's the checksum for files
        uploaded using the satoshi uploader
        does not work without the full file
        """
        length, checksum, data = satoshi.length_checksum_data_from_rawdata(data)
        return satoshi.verify_checksum_data(checksum, data)
