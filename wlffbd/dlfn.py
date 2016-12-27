# -*- coding: utf-8 -*-
'''dlfn class and methods'''
from __future__ import print_function

from . import satoshi
from .blockchaininfo import get_blockchain_request, get_data_online
import blockchainrpc as rpc
from .filesystem import read, readlines, write, newline
from .search import search_hex, search_hashes

from binascii import unhexlify, crc32
from timeit import default_timer as timer

import struct
import zlib

RPCUSER, RPCPASS = read('rpclogin.txt', 'rb').split()
SERVER = rpc.make_server(RPCUSER, RPCPASS)

class dlfn():
    FILENAME = ''
    RPCUSER, RPCPASS = read('rpclogin.txt', 'rb').split()
    SERVER = rpc.make_server(RPCUSER, RPCPASS)
    

    def __init__(self, SERVER, FILENAME='file'):
        self.FILENAME = FILENAME

    def save_data(self, transaction, LOCAL, INDIVIDUALFILE=False):
        if INDIVIDUALFILE:
            self.FILENAME = transaction
        if LOCAL: 
            hexdata = rpc.get_data_local(transaction, self.SERVER)
            inhex = rpc.get_indata_local(transaction, self.SERVER)
        else:
            hexdata, inhex = get_data_online(transaction)
        data = satoshi.unhexutf8(hexdata)
        indata = satoshi.unhexutf8(inhex)
        origdata = data

        significanttx = ''
        significanttx += search_hex(hexdata, "output")
        significanttx += search_hex(inhex, "input")
        significanttx += search_hashes(inhex+hexdata)
        if significanttx != '':
            print(transaction + " " + significanttx)
            self.save_file(transaction + " " + significanttx + newline(), "significant.txt")
        try:
            if self.checksum(data):
                significanttx += "Satosi Checksum found"
            length = struct.unpack('<L', data[0:4])[0]
            data = data[8:8+length]
        except struct.error:
            print("String incorrect length for upack:"+transaction)
            # self.save_file(transaction + newline(), "incorrectlength.txt")
            pass
        self.save_file(indata, self.FILENAME+"indata.txt")     # saves the input script
        self.save_file(data, self.FILENAME+"data.txt")         # saves binary data
        self.save_file(origdata, self.FILENAME+"origdata.txt")         # saves all binary data

    def get_tx_list(self, tx_list, LOCAL):
        """This function checks the blockchain for all transactions in the FILENAME document """
        for line in readlines(tx_list):
            blockhash = line.rstrip('\r\n')
            if blockhash:
                self.save_data(blockhash, LOCAL)

    def get_block_tx(self, start, end, LOCAL):
        """This function checks the blockchain for all transactions in the FILENAME document """
        if not end.isdigit():
            end = rpc.get_block_height(self.SERVER)

        for i in range(int(start), int(end)):
            hashlist = rpc.get_block_transactions(i, self.SERVER)
            print("Block number: {0}".format(i))
            for tx in hashlist:
                self.save_data(tx, LOCAL)

    def save_file(self, filename, dataout):
        """
        This saves the data to the chosen
        filename in binary by appending the file
        """
        write(dataout, filename, 'ab')

    def checksum(self, data):
        """
        verify's the checksum for files
        uploaded using the satoshi uploader
        does not work without the full file
        """
        length, checksum, data = satoshi.length_checksum_data_from_rawdata(data)
        return satoshi.verify_checksum_data(checksum, data)

    def crc(self, filename):
        """
        Should be used to determine if filename
        is garbage or is part of the file
        """
        prev = 0
        for eachLine in open(filename, "rb"):
            prev = zlib.crc32(eachLine, prev)
            print (prev)
        return "%X" % (prev & 0xFFFFFFFF)


