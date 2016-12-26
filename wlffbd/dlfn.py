# -*- coding: utf-8 -*-
'''dlfn class and methods'''
from __future__ import print_function

from . import satoshi
from .blockchaininfo import get_blockchain_request
from .filesystem import read, readlines, write
from .search import search_hex, search_hashes

from binascii import unhexlify, crc32
from timeit import default_timer as timer

import platform
import struct
import zlib
import hashlib
import jsonrpclib
import gc


def newline():
    return '\r\n' if platform.system() == "Windows" else '\n'


class dlfn():
    FILENAME = ''
    RPCUSER, RPCPASS = read('rpclogin.txt', 'rb').split()
    SERVER = jsonrpclib.Server("http://{0}:{1}@localhost:8332".format(RPCUSER, RPCPASS))   # RPC Login

    def __init__(self, SERVER, FILENAME='file'):
        self.FILENAME = FILENAME

    def get_block_data(self, start, end):
        """
        Gets transaction data from block ranges
        """
        # blockcount = self.SERVER.getblockcount()     # This will get the total current blocks
        for i in range(int(start), int(end)):
            start = timer()                     # Start a timer to see how long for each block
            print ("Searching block: {0}:".format(i))
            blockhash = self.SERVER.getblockhash(i)  # Gets the block hash from the block index number
            for tx in self.SERVER.getblock(blockhash)['tx']:  # Gets all transactions from block hash
                self.get_data_local(tx)                       # currently checks all transactions for data

            endtimer = timer() - start
            print(endtimer)
            gc.collect()

    def get_data_local(self, transaction, INDIVIDUALFILE=False):
        """
        Downloads data from Bitcoin Core RPC
        """
        if INDIVIDUALFILE:
            self.FILENAME = transaction
        rawTx = self.SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
        tx = self.SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
        hexdata = ''
        inhex = ''
        indata = b''
        data = b''
        for txin in tx['vin']:
            try:
                for inop in txin['scriptSig']['hex'].split():  # Gathers the input script
                    inhex += inop
                    indata += unhexlify(inop.encode('utf8'))
            except KeyError:
                pass
        for txout in tx['vout']:
            for op in txout['scriptPubKey']['asm'].split(' '):  # searches for all OP data
                try:
                    if not op.startswith('OP_') and len(op) >= 40:
                        hexdata += op.encode('utf8')
                        data += unhexlify(op.encode('utf8'))
                except:
                    data += op.encode('utf8')
        
        significanttx = ''
        significanttx += search_hex(hexdata, "output")
        significanttx += search_hex(inhex, "input")
        significanttx += search_hashes(inhex+hexdata)
        if significanttx != '':
            print(transaction + " " + significanttx)
            self.save_file(transaction + " " + significanttx + newline(), "significant.txt")
        self.save_data(data, indata, transaction)
    


    def save_data(self, data, indata, transaction):
        origdata = data
        try:
            length = struct.unpack('<L', data[0:4])[0]
            data = data[8:8+length]
        except struct.error:
            print("String incorrect length for upack:"+transaction)
            # self.save_file(transaction+newline(), "incorrectlength.txt")
            pass
        self.save_file(indata, self.FILENAME+"indata.txt")     # saves the input script
        self.save_file(data, self.FILENAME+"data.txt")         # saves binary data
        self.save_file(origdata, self.FILENAME+"origdata.txt")         # saves all binary data

    def get_data_online(self, transaction, INDIVIDUALFILE=False):
        """
        Downloads the data from blockchain.info
        TODO: Change the data collection to json
        """
        if INDIVIDUALFILE:
            self.FILENAME = transaction
        origdata = b''
        indata = b''
        inhex = ''
        data = b''
        hexdata = ''
        atoutput = False
        inoutput = False
        for line in get_blockchain_request('tx/{}'.format(transaction), show_adv='true'):

            if b'Output Scripts' in line:
                atoutput = True

            if b'Input Scripts' in line:
                inoutput = False

            if b'</table>' in line:
                atoutput = False
                inouptut = False

            if inoutput:
                if len(line) > 100:
                    chunks = line.split(b' ')
                    for c in chunks:
                        print(c)
                        if b'O' not in c and b'\n' not in c and b'>' not in c and b'<' not in c:
                            inhex += c
                            indata += unhexlify(c.encode('utf8'))

            if atoutput:
                if len(line) > 100:
                    chunks = line.split(b' ')
                    for c in chunks:
                        if b'O' not in c and b'\n' not in c and b'>' not in c and b'<' not in c:
                            hexdata += c
                            data += unhexlify(c)

        significanttx = ''
        significanttx += search_hex(hexdata, transaction, "output")
        significanttx += search_hex(inhex, transaction, "input")
        significanttx += search_hashes(inhex+hexdata, transaction)
        if significanttx != '':
            print(significanttx)
            self.save_file(significanttx + newline(), "significant.txt")
        self.save_data(data, indata, transaction)

    def get_tx_list(self, tx_list, LOCAL=False):
        """This function checks the blockchain for all transactions in the FILENAME document """
        for line in readlines(tx_list):
            blockhash = line.rstrip('\r\n')
            if blockhash:
                if LOCAL:
                    self.get_data_local(blockhash)
                else:
                    self.get_data_online(blockhash)

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

    def sha256_sum(self, data):
        """
        Builds and checks a list of hashes from data
        downloaded from the blockchain
        useful to find duplicate data
        figure out how to save as dictionary file

        """
        hashsum = hashlib.sha256(data)
        hashexists = False
        with open("hashindex.txt", "a+") as hashfile:
            for hashes in hashfile:
                if hashsum.hexdigest() == hashes.strip():
                    hashexists = True

            if not hashexists:
                hashfile.writelines(hashsum.hexdigest()+newline())
                hashexists = False
        hashfile.close()
        return hashexists
