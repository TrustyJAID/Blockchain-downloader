# -*- coding: utf-8 -*-
'''blockchaininfo test functions'''

from wlffbd import blockchaininfo
from mock import patch, Mock

import pytest

import urllib.request, urllib.error, urllib.parse


def test_make_blockchain_url():
    assert 'https://blockchain.info/test?foo=bar&six=9' == blockchaininfo.make_blockchain_url('test', foo='bar', six=9)


@patch('wlffbd.blockchaininfo.urllib2.urlopen')
def test_get_blockchain_request(mock_urlopen):
    mock_urlopen.return_value = Mock()
    mock_urlopen.return_value.read.side_effect = ['test']
    response = blockchaininfo.get_blockchain_request('test', format='json')
    assert 'test' == response.read()


@patch('wlffbd.blockchaininfo.urllib2.urlopen')
def test_get_blockchain_rawaddr(mock_urlopen):
    json = Mock()
    json.read.side_effect = ['{}', '{"simple": "json"}', '{"key": "value"}', '{"key": "value"}']
    mock_urlopen.return_value = json
    assert {} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    assert {'simple': 'json'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    assert {'key': 'value'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    assert {'key': 'value'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef', silent=False)

@patch('wlffbd.blockchaininfo.urllib2.urlopen')
def test_get_blockchain_rawaddr_urlerror(mock_urlopen):
    json = Mock()
    json.read.side_effect = ['{"key": "value"}', '{"key": "value"}']
    mock_urlopen.side_effect = [urllib.error.URLError('Test Error'), json]
    assert {'key': 'value'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef', silent=False)


def test_get_txs_from_blockchain_json():
    assert ['0123456789abcdef'] == blockchaininfo.get_txs_from_blockchain_json({'txs':[{'hash': '0123456789abcdef'}]})
    assert 10 == len(blockchaininfo.get_txs_from_blockchain_json({'txs':[{'hash': str(x)} for x in range(10)]}))


@patch('wlffbd.blockchaininfo.urllib2.urlopen')
@patch('wlffbd.blockchaininfo.time.sleep')
def test_get_tx_from_online(mock_sleep, mock_urlopen):
    mock_urlopen.return_value = Mock()
    mock_urlopen.return_value.read.side_effect = ['{"n_tx": 9, "txs": [{"hash": "0"}, {"hash": "1"}, {"hash": "2"}]}'] * 3
    def _callback(txlist, n_tx):
        assert len(txlist) < n_tx
    blockchaininfo.get_tx_from_online('1234567890abcdef', limit=3, sleep=1, callback=_callback)

'''
def test_get_data_online():
    Page = "Output Scripts somerandomhexvalues"
    # Page.getrawtransaction.return_value = 'raw return value here'
    # Page.decoderawtransaction.return_value = {"vout": [{"value": 1,"n": 0,"scriptPubKey": {"asm": "OP_DUP cad3e1794b73c2d940eefcc29cd55f44eab95d95 OP_CHECKSIG","hex": "abcdef","reqSigs": 1,"type": "pubkeyhash","addresses": ["1walletidthatisblank"]}}, ]}
    hexdata = 'somerandomhexvalues'
    assert hexdata == blockchaininfo.get_data_online('somerandomhexvalues', Page=Page)


def test_get_indata_online():
    SERVER = Mock()
    SERVER.getrawtransaction.return_value = 'raw return value here'
    SERVER.decoderawtransaction.return_value = {"vin": [ {"txid": "somerandomtx","vout": 1,"scriptSig": {"asm": "thiscanbeanything","hex": "somethingbelongsherethatiswaymorethan40characters"},"sequence": 1}]}    
    hexdata = 'somethingbelongsherethatiswaymorethan40characters'
    assert hexdata == blockchaininfo.get_indata_online('somethingbelongsherethatiswaymorethan40characters', SERVER=SERVER)
    '''
