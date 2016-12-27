# -*- coding: utf-8 -*-
'''blockchaininfo test functions'''

from wlffbd import blockchainrpc
from mock import patch, Mock

import pytest

def test_true():
    assert True == True


def test_get_data_local():
    SERVER = Mock()
    SERVER.getrawtransaction.return_value = 'raw return value here'
    SERVER.decoderawtransaction.return_value = {"vout": [{"value": 1,"n": 0,"scriptPubKey": {"asm": "OP_DUP cad3e1794b73c2d940eefcc29cd55f44eab95d95 OP_CHECKSIG","hex": "abcdef","reqSigs": 1,"type": "pubkeyhash","addresses": ["1walletidthatisblank"]}}, ]}
    hexdata = 'cad3e1794b73c2d940eefcc29cd55f44eab95d95'
    assert hexdata == blockchainrpc.get_data_local('cad3e1794b73c2d940eefcc29cd55f44eab95d95', SERVER=SERVER)

def test_get_indata_local():
    SERVER = Mock()
    SERVER.getrawtransaction.return_value = 'raw return value here'
    SERVER.decoderawtransaction.return_value = {"vin": [ {"txid": "somerandomtx","vout": 1,"scriptSig": {"asm": "thiscanbeanything","hex": "somethingbelongsherethatiswaymorethan40characters"},"sequence": 1}]}    
    hexdata = 'somethingbelongsherethatiswaymorethan40characters'
    assert hexdata == blockchainrpc.get_indata_local('somethingbelongsherethatiswaymorethan40characters', SERVER=SERVER)
        

def test_get_block_height():
    SERVER = Mock()
    SERVER.getblockcount.return_value = 123456
    assert 123456 == blockchainrpc.get_block_height(SERVER)

def test_get_block_transactions():
    SERVER = Mock()
    SERVER.blockhash.return_value = 1
    SERVER.getblock.return_value = {'tx':[12, 123, 1234]}
    assert [12, 123, 1234] == blockchainrpc.get_block_transactions(1, SERVER)
