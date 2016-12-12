#!/usr/bin/env python2
from __future__ import print_function
import sys
import struct
from binascii import unhexlify, crc32
import urllib2
import imp
import pip
from timeit import default_timer as timer
import platform
import json
import time
import re
try:
    imp.find_module('jsonrpclib')
except ImportError:
    pip.main(['install', 'jsonrpclib'])
import jsonrpclib
'''There are some things to fix like the length of the
transactions and adding wallet search but this should
work for any previous file on the blockchain. The list
of transactions must also end with a blank line and
'''

SERVER = jsonrpclib.Server("http://User:Passg@localhost:8332")   # RPC Login
BLOCKCHAINADDRESS = ''
global FILENAME
FILENAME = 'file'
INDIVIDUALFILE = False
try:
    # Checks for an RPC connection to local blockchain
    SERVER.getinfo()
    LOCAL = True
except Exception, e:
    print("RPC connection not available")
    LOCAL = False


class dlfn():

    def get_tx_from_online(self, address):
        error = True

        print("Fetching transactions from", address)
        while error:
            try:
                dat = urllib2.urlopen("https://blockchain.info/rawaddr/" + address)
                error = False
            except:
                print("Trying to open address", address)
                time.sleep(4)
        n_tx = json.loads(dat.read().decode())["n_tx"]

        txlist = []
        offset = 0
        while True:
            try:
                dat = urllib2.urlopen("https://blockchain.info/rawaddr/" + address + "?format=json&limit=50&offset=" + str(offset))
                txs = json.loads(dat.read().decode())["txs"]
                dat.close()
                for tx in txs:
                    txlist.append(tx["hash"].encode('ascii'))
                offset += 50
            except:
                pass

            if len(txlist) == n_tx:
                break
            print("Progress (if it gets 'stuck' wait a minute or two):", len(txlist), "/", n_tx)

        return txlist

    def get_block_data(self, start, end):
        # This was supposed to go through each block one by one
        # Then it would check each transaction in each block 
        # looking for one with a scriptPubKey that matches the 
        # wallet ID asked for but this takes a long timer
        # I ran it on 1400 blocks and it took 7 hours to complete
        # blockcount = SERVER.getblockcount()     # This will get the total current blocks
        for i in range(start, end):
            start = timer()                     # Start a timer to see how long for each block
            # print ("Searching block: {0} for wallet: {1} for wallet: ".format(i, walletid))
            blockhash = SERVER.getblockhash(i)  # Gets the block hash from the block index number
            for tx in SERVER.getblock(blockhash)['tx']:  # Gets all transactions from block hash
                # print(tx)                                 # Prints all transactions checked
                dlfn.get_data_local(tx)                       # currently checks all transactions for data

            endtimer = timer() - start
            print(endtimer)

    def get_data_local(self, transaction):
        """
        Decodes an individual
        transaction using local blockchain
        """
        if INDIVIDUALFILE:
            global FILENAME
            FILENAME = transaction
        rawTx = SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
        tx = SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
        hexdata = ''                                    # string for collecting hex data
        data = b''                                      # binary data
        regexsearch = ''
        for txout in tx['vout']:                  # Searches json for all vout, failed a few times
            if regexsearch != '':
                self.regex_pattern(regexsearch)
                regexsearch = ''

            for op in txout['scriptPubKey']['asm'].split(' '):  # searches for all OP data
                regexsearch += op
                try:
                    if not op.startswith('OP_') and len(op) >= 40:
                        hexdata += op.encode('utf8')
                        data += unhexlify(op.encode('utf8'))
                except:
                    data += op.encode('utf8')

        print(transaction + chkfn().check_magic(hexdata), end='\r')  # would have liked multi line prints
        try:                                            # a lot of transactions failed here trying to
            length = struct.unpack('<L', data[0:4])[0]  # unpack the binary data so I added parameters
            data = data[8:8+length]                     # to try and extract all data
            self.save_file(hexdata, FILENAME+"hex.txt")       # saves all hex data
            self.save_file(data, FILENAME+"data.txt")         # saves all binary data
            if platform.system() == "Windows":
                self.save_file(transaction+chkfn().check_magic(hexdata)+"\r\n", "headerfiles.txt")  # creates a file of transactions and headers
            else:
                self.save_file(transaction+chkfn().check_magic(hexdata)+"\n", "headerfiles.txt")
            return data
        except:
            self.save_file(hexdata, FILENAME+"fhex.txt")      # This is here to save files when the unpack fails
            self.save_file(data, FILENAME+"fdata.txt")        # if we can figure out how to solve the unpacking
            if platform.system() == "Windows":
                self.save_file(transaction+chkfn().check_magic(hexdata)+"\r\n", "headerfiles.txt")
            else:
                self.save_file(transaction+chkfn().check_magic(hexdata)+"\n", "headerfiles.txt")
            return data

    def regex_pattern(self, data):
        pattern = r"(?:^| )[0-9a-fA-F]+(?:$| )"
        matchList = []
        matchList += re.search(pattern, data)
        return matchList

    def get_data_online(self, transaction):
        """
        This function checks the data
        in the given blockhash using blockchain.info
        """
        if INDIVIDUALFILE:
            global FILENAME
            FILENAME = transaction
        url = ('https://blockchain.info/tx/%s?show_adv=true' % str(transaction))
        dataout = urllib2.urlopen(url)
        odata = b''
        data = b''
        hexdata = ''
        atoutput = False
        for line in dataout:

            if b'Output Scripts' in line:
                atoutput = True

            if b'</table>' in line:
                atoutput = False

            if atoutput:
                if len(line) > 100:
                    chunks = line.split(b' ')
                    for c in chunks:
                        if b'O' not in c and b'\n' not in c and b'>' not in c and b'<' not in c:
                            hexdata += c
                            data += unhexlify(c)

        odata += data
        length = struct.unpack('<L', data[0:4])[0]
        data = data[8:8+length]
        if chkfn().check_magic(hexdata) != '':
            print(chkfn().check_magic(hexdata))

        self.save_file(odata, FILENAME+"o")
        self.save_file(data, FILENAME)
        if platform.system() == "Windows":
            self.save_file(transaction+chkfn().check_magic(hexdata)+"\r\n", "headerfiles.txt")
        else:
            self.save_file(transaction+chkfn().check_magic(hexdata)+"\n", "headerfiles.txt")
        return data

    def get_tx_list(self, tx_list):
        """
        This function checks the blockchain
        for all transactions in the FILENAME document
        """
        with open(tx_list) as f:
            transaction = f.readlines()
        for i in range(len(transaction)):
            blockhash = transaction[i].rstrip('\r\n')
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
        output.close()


class chkfn():

    counter = 0
    hexcode2 = ''
    hexcoderev = ''

    def check_magic(self, hexcode):
        """
        This is the hex header search function
        It searches the line of hex
        for any of these known header hex values
        Todo: add private PGP 2048, 4096, 8192 headers
        also add two transaction hex search in cases
        where header data is split between two transactions
        first attempt was to concactenate all hex data every time
        but that took a long time to do. At most two or three transactions
        will contain the header
        Also it might be worth adding more function to the names
        such as including all possible capitalization hex
        TODO: finish double transaction check and reverse header search
        """
        self.hexcode2 += hexcode
        if self.counter == 1:
            self.counter = 0

        filetype = ''
        if "D0CF11E0A1B11AE1".lower() in hexcode:
            filetype += "DOC Header Found "         # DOC Header
        if "576F72642E446F63756D656E742E".lower() in hexcode:
            filetype += "DOC Footer Found "         # DOC Footer
        if "D0CF11E0A1B11AE1".lower() in hexcode:
            filetype += "XLS Header Found "         # XLS Header
        if "FEFFFFFF000000000000000057006F0072006B0062006F006F006B00".lower() in hexcode:
            filetype += "XLS Footer Found "         # XLS Footer
        if "D0CF11E0A1B11AE1".lower() in hexcode:
            filetype += "PPT Header Found "         # PPT Header
        if "A0461DF0".lower() in hexcode:
            filetype += "PPT Footer Found "         # PPT Footer
        if "504B030414".lower() in hexcode:
            filetype += "ZIP Header Found "         # ZIP Header
        if "504B050600".lower() in hexcode:
            filetype += "ZIP Footer Found "         # ZIP Footer
        if "504B030414000100630000000000".lower() in hexcode:
            filetype += "ZIPLock Footer Found "     # ZLocked Encrypted
        if "FFD8FFE000104A464946000101".lower() in hexcode:
            filetype += "JPG Header Found "         # JPG Header
        if "474946383961".lower() in hexcode:
            filetype += "GIF Header Found "         # GIF Header
        if "474946383761".lower() in hexcode:
            filetype += "GIF Header Found "         # GIF Header
        if "2100003B00".lower() in hexcode:
            filetype += "GIF Footer Found "         # GIF Footer
        if "25504446".lower() in hexcode:
            filetype += "PDF Header Found "         # PDF Header
        if "2623323035".lower() in hexcode:
            filetype += "PDF Header Found "         # PDF Header
        if "2525454F46".lower() in hexcode:
            filetype += "PDF Footer Found "         # PDF Footer
        if "616E6E6F756E6365".lower() in hexcode:
            filetype += "Torrent Header Found "     # Torrent Header
        if "1F8B".lower() in hexcode:
            filetype += ".TAR.GZ Header Found "     # TAR/GZ Header | Going to have lots of false positives
        if "0011AF".lower() in hexcode:
            filetype += "FLI Header Found "         # FLI Header
        if "504B03040A000200".lower() in hexcode:
            filetype += "EPUB Header Found "        # EPUB Header
        if "89504E470D0A1A0A".lower() in hexcode:
            filetype += "PNG Header Found "         # PNG Header
        if "6D51514E42".lower() in hexcode:
            filetype += "8192PGP Header Found "     # 8192 Header
        if "6D51494E4246672F".lower() in hexcode:
            filetype += "4096PGP Header Found "     # 4096 Header
        if "952e3e2e584b7a".lower() in hexcode:
            filetype += "2048PGP Header Found "     # 2048 Header
        if "526172211A0700".lower() in hexcode:
            filetype += "Secret Header Found"       # Secret Header
        if "6D51454E424667".lower() in hexcode:
            filetype += "RAR Header Found"          # RAR Header
        if "EFEDFACE".lower() in hexcode:
            filetype += "UTF8 Header Found"         # UTF8 header
        if "4F676753".lower() in hexcode:
            filetype += "OGG Header Found"          # OGG Header
        if "42494646".lower() in hexcode and "57415645".lower() in hexcode:
            filetype += "WAV Header Found"          # WAV Header
        if "42494646".lower() in hexcode and "41564920".lower() in hexcode:
            filetype += "AVI Header Found"          # AVI Header
        if "4D546864".lower() in hexcode:
            filetype += "MIDI Header Found"         # MIDI Header
        if "377ABCAF271C".lower() in hexcode:
            filetype += "7z Header Found"           # 7z Header
        if "0000001706".lower() in hexcode:
            filetype += "7z Footer Found"           # 7z Footer
        if "57696b696c65616b73".lower() in hexcode:
            filetype += "Wikileaks"                 # Wikileaks
        if "4A756C69616E20417373616E6765".lower() in hexcode:
            filetype += "Julian Assange"            # Julain Assange
        if "4d656e646178".lower() in hexcode:
            filetype += "Mendax"                    # Mendax
        else:
            filetype += ""
        chkfn.counter += 1
        return filetype

    def checksum(self, data):
        """
        Checksum for multi file upload data
        """

        checksum = struct.unpack('<L', data[4:8])[0]
        if checksum != crc32(data):
            print('Checksum mismatch; expected %d but calculated %d' % (checksum, crc32(data)))
        return checksum


class __main__():
    """
    Start of the main program
    This could theoretically all be made in a GUI
    """
    dlfn = dlfn()
    if len(sys.argv) == 3:
        # This checks if two arguments were given and
        # utilises them as the transaction then the filename to save
        try:
            BLOCKCHAINADDRESS = str(sys.argv[1])
            FILENAME = str(sys.argv[2])
        except IndexError:
            print("No address of filename")

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
        BLOCKCHAINADDRESS = raw_input('Enter the blockchain Address or transactions file:')
        FILENAME = raw_input('Enter the file name you would like to save to')
        if FILENAME == '':
            # This gives a default filename
            FILENAME = 'file.txt'

    if BLOCKCHAINADDRESS.endswith(".txt"):
        # This checks if you're giving a list of transactions or just one
        dlfn.get_tx_list(BLOCKCHAINADDRESS)

    elif BLOCKCHAINADDRESS.isdigit() and BLOCKCHAINADDRESS < SERVER.getblockheight() and LOCAL:
        if len(sys.argv) == 3:
            dlfn.get_block_data(sys.argv[1], sys.argv[2])
        else:
            dlfn.get_block_data(sys.argv[1], SERVER.getblockheight())

    elif len(BLOCKCHAINADDRESS) < 64 and BLOCKCHAINADDRESS.startswith('1'):
        # Checks if wallet on main blockchain
        print("This is a wallet ID, searching...")
        dlfn.get_tx_from_online(BLOCKCHAINADDRESS)

    else:
        if LOCAL:
            dlfn.get_data_local(BLOCKCHAINADDRESS)
        else:
            dlfn.get_data_online(BLOCKCHAINADDRESS)

