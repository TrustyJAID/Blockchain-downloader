# -*- coding: utf-8 -*-
'''dlfn class and methods'''
from __future__ import print_function

from .blockchaininfo import get_blockchain_request
from .magic import check_magic

from binascii import unhexlify, crc32
from timeit import default_timer as timer

import platform
import struct
import urllib2
import zlib
import hashlib
import jsonrpclib


def newline():
        return '\r\n' if platform.system() == "Windows" else '\n'


class dlfn():
    FILENAME = ''
    RPCUSER, RPCPASS = open('rpclogin.txt', 'rb').read().split()
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
            print ("Searching block: {0}: ".format(i), end='\r')
            blockhash = self.SERVER.getblockhash(i)  # Gets the block hash from the block index number
            for tx in self.SERVER.getblock(blockhash)['tx']:  # Gets all transactions from block hash
                self.get_data_local(tx)                       # currently checks all transactions for data

            endtimer = timer() - start
            print(endtimer)

    def get_data_local(self, transaction, INDIVIDUALFILE=False):
        """
        Downloads data from Bitcoin Core RPC
        """
        if INDIVIDUALFILE:
            self.FILENAME = transaction
        rawTx = self.SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
        tx = self.SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
        hexdata = ''
        revhex = ''
        inhex = ''
        indata = b''
        data = b''
        origdata = ''
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

        revhex = "".join(reversed([hexdata[i:i+2] for i in range(0, len(hexdata), 2)]))  # reverses the hex
        origdata = data  # keeps the original data without modifying it
        length = struct.unpack('<L', data[0:4])[0]
        data = data[8:8+length]
        # self.checksum(data)
        self.save_file(indata, self.FILENAME+"indata.txt")     # saves the input script
        # self.save_file(inhex, self.FILENAME+"inhex.txt")     # saves the input hex
        # self.save_file(hexdata, self.FILENAME+"hex.txt")       # saves all hex data
        self.save_file(data, self.FILENAME+"data.txt")         # saves binary data
        self.save_file(origdata, self.FILENAME+"origdata.txt")         # saves all binary data
        if check_magic(hexdata) != '':
            print(transaction + check_magic(hexdata)+" output")
            self.save_file(transaction + check_magic(hexdata) + newline(), "headerfiles.txt")
        if check_magic(revhex) != '':
            print(transaction + check_magic(revhex)+" reverse")
            self.save_file(transaction + check_magic(inhex) + newline(), "revheaderfiles.txt")
        if check_magic(inhex) != '':
            print(transaction + check_magic(inhex)+" input")
            self.save_file(transaction + check_magic(inhex) + newline(), "inheaderfiles.txt")
        if self.sha256_sum(data):
            print("This output hash already exists in the list")
        if self.sha256_sum(indata):
            print("This intput hash already exists in the list")

        return data

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

        origdata += data
        length = struct.unpack('<L', data[0:4])[0]
        data = data[8:8+length]
        if check_magic(hexdata) != '':
            print(check_magic(inhex)+" input")
            print(check_magic(hexdata)+" output")

        self.save_file(origdata, self.FILENAME+"orig.txt")
        self.save_file(data, self.FILENAME+".txt")
        self.save_file(indata, self.FILENAME+"in.txt")
        self.save_file(transaction+check_magic(hexdata)+newline(), "headerfiles.txt")

    def get_tx_list(self, tx_list, LOCAL=False):
        """
        This function checks the blockchain
        for all transactions in the FILENAME document
        """
        with open(tx_list) as f:
            transaction = f.readlines()
        for i in range(len(transaction)):
            blockhash = transaction[i].rstrip('\r\n')
            print((type(blockhash), blockhash))
            if (blockhash != ''):
                if LOCAL:
                    self.get_data_local(blockhash)
                else:
                    self.get_data_online(blockhash)

    def save_file(self, dataout, filename):
        """
        This saves the data to the chosen
        filename in binary by appending the file
        """
        with open(filename, "ab") as output:
            output.write(dataout)

    def checksum(self, data):
        """
        verify's the checksum for files
        uploaded using the satoshi uploader
        does not work without the full file
        """
        checksum = struct.unpack('<L', data[4:8])[0]
        if checksum != crc32(data):
            print('Checksum mismatch; expected %d but calculated %d' % (checksum, crc32(data)))
        return checksum

    def crc(self, data):
        """
        Should be used to determine if data
        is garbage or is part of the file
        """
        prev = 0
        for eachLine in open(data, "rb"):
            prev = zlib.crc32(eachLine, prev)
            print (prev)
        return "%X" % (prev & 0xFFFFFFFF)

    def sha256_sum(self, data):
        """
        Builds and checks a list of hashes from data
        downloaded from the blockchain
        useful to find duplicate data
        although the more I think about ite
        the less likely I think it's possible
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
