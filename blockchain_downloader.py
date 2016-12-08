#!usr/bin/python2
# https://gist.github.com/shirriff/64f48fa09a61b56ffcf9#file-bitcoin-file-downloader-py
# 
# This code has been modified from several sources and is free to use
# Install Python 2.7.12
# Install pip on windows
# https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
# Install pip on linux $ sudo apt-get install python-pip
# During install when it asks for what modules to install
# ensure that the last option install to PATH is enabled
# After installing run Command Prompt/Terminal
# Change directory to where the file is saved
# Type: python blockchain_downloader.py
# You can add the transaction after or it will ask
# for one upon start if one isn't supplied
# You can also add a filename to save it as after the transaction
# The dafault filename is 'file'
# If you have the bitcoin RPC service setup with a
# local blockchain add it to the RPC settings at the top
from __future__ import print_function
import sys
import struct
from binascii import unhexlify, crc32
import urllib2
import imp
import pip
from timeit import default_timer as timer
import time
import json

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


RPCSERVER = "http://User:Pass@localhost:8332"

SERVER = jsonrpclib.Server(RPCSERVER)

PRINTDATA = True  # Lets you see file output in terminal


try:
    # Checks for an RPC connection
    SERVER.getinfo()
    LOCAL = True
except Exception, e:
    print("RPC connection not available")
    LOCAL = False

def get_tx_from_addr(address):
    error = True
    
    print("Fetching transactions from", address)
    while error:
        try: 
            dat = urllib2.urlopen("https://blockchain.info/rawaddr/" + address)
            error = False
        except:
            print("Trying to open address", address)
            time.sleep(4)
    n_tx = json.loads( dat.read().decode() )["n_tx"]


    txlist = []
    offset = 0
    while True:
        try:
            dat = urllib2.urlopen("https://blockchain.info/rawaddr/" + address + "?format=json&limit=50&offset="+ str(offset) )
            txs = json.loads( dat.read().decode() )["txs"]
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

def gettxfromwallet2(walletid):
    for tx in get_tx_from_addr(walletid):
        printdataoutlocal(tx)

# @cuda.jit(device='gpu')
def gettxfromwallet(walletid):

    blockcount = SERVER.getblockcount()
    for i in range(441786, 441785, -1): # 434504-434764 435170 - 435350
        start = timer()
        #print ("Searching block: {0} for wallet: {1} for wallet: ".format(i, walletid))
        blockhash = SERVER.getblockhash(i)
        for tx in SERVER.getblock(blockhash)['tx']:
            #print(tx)
            printdataoutlocal(tx)
            # print(transaction['vout'][0:-2])
            #for var in transaction['vout'][0:-2]:
                # print (var)
                #savefile(str(var))
                #for address in var['scriptPubKey']['addresses']:
                    # print(address)
                #    if address == walletid:
                #        print("Found the wallet")
        endtimer = timer() - start
        print(endtimer)


def printdataoutlocal(transaction):
    '''Decodes an individual transaction using local blockchain'''
    rawTx = SERVER.getrawtransaction(transaction)
    tx = SERVER.decoderawtransaction(rawTx)
    hexdata = ''
    ohexdata=''
    data = b''
    odata = b''
    # print(tx)
    for txout in tx['vout']:
        #print(txout)
        for op in txout['scriptPubKey']['asm'].split(' '):
            # print (op)
            try:
                hexdata += op.encode('utf8')
                data += unhexlify(op.encode('utf8'))
                if not op.startswith('OP_') and len(op) >= 40:
                    ohexdata += op.encode('utf8')
                    odata += unhexlify(op.encode('utf8'))
            except:
                data += op.encode('utf8')

    print(transaction + checkheader(hexdata), end='\r')
    #checksum(data)
    try:
        length = struct.unpack('<L', data[0:4])[0]
        data = data[8:8+length]
        length = struct.unpack('<L', odata[0:4])[0]
        odata = odata[8:8+length]
        savefile(hexdata, FILENAME+"hex.txt")
        savefile(data, FILENAME+"data.txt")
        savefile(odata, FILENAME+"odata.txt")
        savefile(ohexdata, FILENAME+"ohex.txt")
        savefile(transaction+checkheader(hexdata)+"\r\n", "headerfiles.txt")
        return data
    except:
        savefile(hexdata, FILENAME+"fhex.txt")
        savefile(data, FILENAME+"fdata.txt")
        savefile(odata, FILENAME+"fodata.txt")
        savefile(ohexdata, FILENAME+"fohexdata.txt")
        savefile(transaction+checkheader(hexdata)+"\r\n", "headerfiles.txt")
        return data


def checksum(data):

    checksum = struct.unpack('<L', data[4:8])[0]
    # This was left in from the original script, it doesn't work correctly'
    if checksum != crc32(data):
        print('Checksum mismatch; expected %d but calculated %d' % (checksum, crc32(data)))
    # sys.exit()


def printdataoutonline(transaction):
    """This function checks the data
    in the given blockhash using blockchain.info"""

    url = ('https://blockchain.info/tx/%s?show_adv=true' % str(transaction))
    dataout = urllib2.urlopen(url)
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

    #checksum(data)
    length = struct.unpack('<L', data[0:4])[0]
    data = data[8:8+length]
    if checkheader(hexdata) != '':
        print(checkheader(hexdata))

    savefile(data, FILENAME)
    savefile(checkheader(hexdata)+transaction, "headerfiles.txt")
    # sys.stdout.buffer.write(dataout)
    #if PRINTDATA:
        #print (data)
    return data


def fileofblocks():
    """This function checks the blockchain
    for all files in the FILENAME document"""
    with open(BLOCKCHAINADDRESS) as f:
        transaction = f.readlines()
        # FILENAME = transaction
    for i in range(len(transaction)):
        # print(len(transaction))
        blockhash = transaction[i].rstrip('\r\n')

        if (blockhash == ''):
            break

        if LOCAL:
            printdataoutlocal(blockhash)
        else:
            printdataoutonline(blockhash)


def savefile(dataout, filename):
    """This saves the data to the chosen
    filename in binary by overwriting the file """

    with open(filename, "ab") as output:
        output.write(dataout)
    output.close()


def checkheader(hexcode):
    #    if "99".lower() in hexcode:
    #        filetype += "GPG Header Found "    # GPG Header| Commented out 
    #    if "9901".lower() in hexcode:
    #        filetype += "PKR Header Found "    # PKR Header| to reduce positives
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
    if "1F8B08".lower() in hexcode:
        filetype += ".TAR.GZ Header Found "     # TAR/GZ Header
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
    if "6D51454E424667".lower() in hexcode:
        filetype += "2048PGP Header Found "     # 2048 Header
    if "526172211A0700".lower() in hexcode:
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
    if "57696b696c65616b73".lower() in hexcode:
        filetype += "Wikileaks"                 # Wikileaks
    if "4A756C69616E20417373616E6765".lower() in hexcode:
        filetype += "Julian Assange"            # Julain Assange
    else:
        filetype += ""
    return filetype


# This is the start of the program


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
        FILENAME = 'file'


if BLOCKCHAINADDRESS.endswith(".txt"):
    # This checks if you're giving a list of transactions or just one
    fileofblocks()

elif len(BLOCKCHAINADDRESS) < 64:
    # This will check if tx or wallet
    print("This is a wallet ID, searching...")
    gettxfromwallet(BLOCKCHAINADDRESS)

else:
    if LOCAL:
        printdataoutlocal(BLOCKCHAINADDRESS)

    else:
        printdataoutonline(BLOCKCHAINADDRESS)

