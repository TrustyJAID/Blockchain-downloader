#!/usr/bin/env python3

from __future__ import print_function
from wlffbd.blockchaininfo import get_tx_from_online
from wlffbd.blockchainrpc import make_server
from . import satoshi
from . import blockchaininfo as online
from . import blockchainrpc as rpc
from .filesystem import read, readlines, write, newline
from .search import search_hex, check_hash, search_words, get_extension

import json
import sys
import time
import jsonrpclib
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

RPCUSER, RPCPASS = open('rpclogin.txt', 'r').read().split()

class Blockchain_GUI:              
    def __init__(self, master):
        self.master = master
        self.local = False
        self.server = None
        master.title("Blockchain Downloader")
        self.binary_area = Text(wrap=WORD, width=50)
        self.binary_area.grid(row= 4, column= 0, columnspan= 2)
        self.bin_scrollbar = Scrollbar(orient=VERTICAL, command=self.binary_area.yview)
        self.bin_scrollbar.grid(row= 4, column= 2, sticky=N+S)
        self.binary_area["yscrollcommand"]  =  self.bin_scrollbar.set

        self.hex_area = Text(wrap=WORD, width=50)
        self.hex_area.grid(row= 4,column= 3, columnspan= 2)
        self.hex_scrollbar = Scrollbar(orient=VERTICAL, command=self.hex_area.yview)
        self.hex_scrollbar.grid(row=4, column=8, sticky=N+S)
        self.hex_area["yscrollcommand"]  =  self.hex_scrollbar.set

        self.transaction = Entry( width= 65)
        self.transaction.grid(row=2, column=3)
        self.tx_label = Label(text="Transaction")
        self.tx_label.grid(row=0, column=3)
        self.search_button = Button(text="Search", command=self.get_data)
        self.search_button.grid(row= 1, column=3)

        self.user_label = Label(text="RPC Username")
        self.user_label.grid(row=0, column=0)
        self.pass_label = Label(text="RPC Username")
        self.pass_label.grid(row=0, column=1)
        self.rpc_button = Button(text="Connect", command=self.rpc_connect)
        self.rpc_button.grid(row= 2, column=0)
        self.connection_label = Label(text="Not Connected")
        self.connection_label.grid(row=2, column=1)
        self.rpc_username = Entry()
        self.rpc_username.grid(row=1, column=0)
        self.rpc_username.insert(0, RPCUSER)# RPCUSER
        self.rpc_password = Entry(show="*")
        self.rpc_password.grid(row=1, column=1)
        self.rpc_password.insert(0, RPCPASS)# = RPCPASS

    def get_data(self):
        transaction = self.transaction.get()
        if self.local:
            hexdata = rpc.get_data_local(transaction, self.server)
            inhex = rpc.get_indata_local(transaction, self.server)
        else:
            page = online.get_blockchain_transaction_json(transaction)
            hexdata = online.get_data_online(page)
            inhex = online.get_indata_online(page)
        origindata = satoshi.unhexutf8(inhex)
        origdata = satoshi.unhexutf8(hexdata)
        # print(hexdata[-700:] + "\n\n\n" + hexdata2[-700:])
        _, _, data = satoshi.length_checksum_data_from_rawdata(origdata)
        _, _, indata = satoshi.length_checksum_data_from_rawdata(origindata)
        significanttx = ''
        significanttx += search_hex(hexdata, " output")
        significanttx += search_hex(inhex, " input")
        # significanttx += check_hash(inhex+hexdata, 'ripemd160')
        if self.checksum(origdata):
            significanttx += " Satoshi Checksum found Output"
        # if self.checksum(origindata):
            # significanttx += " Satoshi Checksum found input"
        if search_words(origdata):
            significanttx += " ASCII letters found output"
            # print(origdata)
        if search_words(origindata):
            significanttx += " ASCII letters found input"
        extension = get_extension(significanttx)
        if "Satoshi" in significanttx:
            write("temp/" + transaction[:5]+"data." + extension, data, True, 'wb')
            self.hex_area.insert(INSERT, data)
        else:
            self.hex_area.insert(INSERT, origdata)
            write("temp/" + transaction[:5]+"origdata." + extension, origdata, True, 'wb')# saves all binary data
        # write("temp/" + transaction[:5]+"indata." + extension, indata, True, 'wb')     # saves the input script
        self.binary_area.insert(INSERT, transaction + "\n\n" + significanttx + "\n\n")
        

    def rpc_connect(self):
        username = self.rpc_username.get()
        password = self.rpc_password.get()
        self.server = make_server(username, password)
        try:
            # Checks for an RPC connection to local blockchain
            self.server.getinfo()
            # self.binary_area.insert(INSERT, self.server.getinfo())
            self.local = True
        except Exception as e:
            print("RPC connection not available")
            self.local = False
        if self.local:
            self.connection_label["text"] = "Connected"

    def checksum(self, data):
        """
        verify's the checksum for files
        uploaded using the satoshi uploader
        does not work without the full file
        """
        length, checksum, data = satoshi.length_checksum_data_from_rawdata(data)
        return satoshi.verify_checksum_data(checksum, data)
