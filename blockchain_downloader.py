#!/usr/bin/env python2
from __future__ import print_function

from binascii import unhexlify, crc32
from timeit import default_timer as timer

import json
import platform
import sys
import struct
import time
import re
import urllib2

try:
    import jsonrpclib
except ImportError:
    print('Fatal: jsonrpclib missing (Try `pip install -r requirements.txt`)')
    sys.exit(-1)

RPCUSER, RPCPASS = 'Damez', 'something'
SERVER = jsonrpclib.Server("http://{0}:{1}@localhost:8332".format(RPCUSER, RPCPASS))   # RPC Login
BLOCKCHAINADDRESS = ''
global FILENAME
FILENAME = 'file'       # global default filename setting
INDIVIDUALFILE = False  # Single flag for single file fore each transaction
try:
    # Checks for an RPC connection to local blockchain
    SERVER.getinfo()
    LOCAL = True
except Exception, e:
    print("RPC connection not available")
    LOCAL = False


def newline():
    return '\r\n' if platform.system() == "Windows" else '\n'


class dlfn():

    def get_block_data(self, start, end):
        """
        Gets transaction data from block ranges
        """
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
        transaction using blockchain RPC
        """
        if INDIVIDUALFILE:
            global FILENAME
            FILENAME = transaction
        rawTx = SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
        tx = SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
        hexdata = ''
        revhex = ''
        inhex = ''
        indata = b''
        data = b''
        origdata = ''
        # regexsearch = ''
        for txin in tx['vin']:
            try:
                for inop in txin['scriptSig']['hex'].split():  # Gathers the input script
                    inhex += inop
                    indata += unhexlify(inop.encode('utf8'))
            except KeyError:
                pass
        for txout in tx['vout']:
            # if regexsearch != '':
                # self.regex_pattern(regexsearch)
                # regexsearch = ''

            for op in txout['scriptPubKey']['asm'].split(' '):  # searches for all OP data
                # regexsearch += op
                try:
                    if not op.startswith('OP_') and len(op) >= 40:
                        hexdata += op.encode('utf8')
                        data += unhexlify(op.encode('utf8'))
                except:
                    data += op.encode('utf8')
        revhex = "".join(reversed([hexdata[i:i+2] for i in range(0, len(hexdata), 2)]))  # reverses the hex
        print(transaction + check_magic(hexdata), end='\r')  # would have liked multi line prints
        print(transaction + check_magic(revhex), end='\r')  # would have liked multi line prints
        origdata = data  # keeps the original data without modifying it
        # try:
        length = struct.unpack('<L', data[0:4])[0]
        data = data[8:8+length]
        self.save_file(indata, FILENAME+"indata.txt")     # saves the input script
        self.save_file(inhex, FILENAME+"inhex.txt")     # saves the input hex
        self.save_file(hexdata, FILENAME+"hex.txt")       # saves all hex data
        self.save_file(data, FILENAME+"data.txt")         # saves binary data
        self.save_file(origdata, FILENAME+"origdata.txt")         # saves all binary data
        self.save_file(transaction + check_magic(hexdata) + newline(), "headerfiles.txt")
        # except:
        #     self.save_file(hexdata, FILENAME+"fhex.txt")      # This is here to save files when the unpack fails
        #     self.save_file(data, FILENAME+"fdata.txt")        # Fails on certain transactions, not normal
        #     self.save_file(origdata, FILENAME+"origdata.txt")         # saves all binary data
        #     self.save_file(transaction + check_magic(hexdata) + newline(), "headerfiles.txt")
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
        origdata = b''
        indata = b''
        inhex = ''
        data = b''
        hexdata = ''
        atoutput = False
        inoutput = False
        for line in dataout:

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

        self.save_file(origdata, FILENAME+"orig.txt")
        self.save_file(data, FILENAME+".txt")
        self.save_file(indata, FILENAME+"in.txt")
        self.save_file(transaction+check_magic(hexdata)+newline(), "headerfiles.txt")

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

    def checksum(self, data):
        """
        Checksum for multi file upload data
        """

        checksum = struct.unpack('<L', data[4:8])[0]
        if checksum != crc32(data):
            print('Checksum mismatch; expected %d but calculated %d' % (checksum, crc32(data)))
        return checksum


DEFAULT_MAGIC = {"DOC Header": ["d0cf11e0a1b11ae1"],
                 "DOC Footer": ["576f72642e446f63756d656e742e"],
                 "XLS Header": ["d0cf11e0a1b11ae1"],
                 "XLS Footer": ["feffffff000000000000000057006f0072006b0062006f006f006b00"],
                 "PPT Header": ["d0cf11e0a1b11ae1"],
                 "PPT Footer": ["a0461df0"],
                 "ZIP Header": ["504b030414"],
                 "ZIP Footer": ["504b050600"],
                 "ZIPLock Footer": ["504b030414000100630000000000"],
                 "JPG Header": ["ffd8ffe000104a464946000101"],
                 "GIF Header": ["474946383961"],
                 "GIF Footer": ["2100003b00"],
                 "PDF Header": ["25504446"],
                 "PDF Header": ["2623323035"],
                 "PDF Footer": ["2525454f46"],
                 "Torrent Header": ["616e6e6f756e6365"],
                 "TAR/GZ Header": ["1f8b"],
                 "FLI Header": ["0011af"],
                 "EPUB Header": ["504b03040a000200"],
                 "PNG Header": ["89504e470d0a1a0a"],
                 "8192 Header": ["6d51514e42"],
                 "4096 Header": ["6d51494e4246672f"],
                 "2048 Header": ["952e3e2e584b7a"],
                 "Secret Header": ["526172211a0700"],
                 "RAR Header": ["6d51454e424667"],
                 "UTF8 header": ["efedface"],
                 "OGG Header": ["4f676753"],
                 "WAV Header": ["42494646", "57415645"],
                 "AVI Header": ["42494646", "41564920"],
                 "MIDI Header": ["4d546864"],
                 "7z Header": ["377abcaf271c"],
                 "7z Footer": ["0000001706"],
                 "Wikileaks": ["57696b696c65616b73"],
                 "Julian Assange": ["4a756c69616e20417373616e6765"],
                 "Mendax": ["4d656e646178"]}


def check_magic(hexcode, magic=DEFAULT_MAGIC):
    '''Returns a string listing magic bytes found in the given hexcode and compared against the magic dictionary of keys to lists of values.

    This is the hex header search function.  It searches the line of hex for any of these known header hex values.
    '''
    return ' '.join('{} Found'.format(key)
                   for key, values in magic.iteritems()
                   if all(v.lower() in hexcode for v in values))


def get_blockchain_rawaddr(address, limit=50, offset=0, silent=True):
    error = True
    while error:
        try:
            dat = urllib2.urlopen('https://blockchain.info/rawaddr/{}?format=json&limit={}&offset={}'.format(address, limit, offset))
            error = False
        except urllib2.URLError, e:
            if not silent:
                print('Error: Trying to open address {} from blockchain.info: '.format(address, e.reason))
    return json.loads(dat.read().decode())


def get_txs_from_blockchain_json(data):
    return [tx.get('hash').encode('ascii') for tx in data.get('txs', {})]


def get_tx_from_online(address, limit=50, sleep=1):
    print("Fetching transactions from", address)

    offset = 0
    data = get_blockchain_rawaddr(address, limit=limit, offset=offset, silent=False)
    n_tx = data['n_tx']
    txlist = get_txs_from_blockchain_json(data)

    while len(txlist) < n_tx:
        print("Progress (if it gets 'stuck' wait a minute or two): {} / {}".format(len(txlist), n_tx))
        offset += 50
        txlist.extend(get_txs_from_blockchain_json(get_blockchain_rawaddr(address, limit=limit, offset=offset, silent=True)))
        # Lets be nice to blockchain.info
        if sleep:
            time.sleep(sleep)

    return txlist


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
        get_tx_from_online(BLOCKCHAINADDRESS)

    else:
        if LOCAL:
            dlfn.get_data_local(BLOCKCHAINADDRESS)
        else:
            dlfn.get_data_online(BLOCKCHAINADDRESS)

