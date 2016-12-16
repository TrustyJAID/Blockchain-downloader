# -*- coding: utf-8 -*-
'''blockchaininfo test functions'''

from wlffbd import blockchaininfo
from mock import patch, Mock

import pytest

import urllib2

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
    # TODO: Make this work
    #mock_urlopen.side_effect = [json, json, urllib2.URLError('Test Error', json]
    mock_urlopen.side_effect = [json, json, json, json]
    assert {} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    assert {'simple': 'json'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    assert {'key': 'value'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef')
    # TODO: Test the printed output for the error, or remove it from these functions to make them pure
    assert {'key': 'value'} == blockchaininfo.get_blockchain_rawaddr('1234567890abcdef', silent=False)


def test_get_txs_from_blockchain_json():
    assert ['0123456789abcdef'] == blockchaininfo.get_txs_from_blockchain_json({'txs':[{'hash': '0123456789abcdef'}]})
    assert 10 == len(blockchaininfo.get_txs_from_blockchain_json({'txs':[{'hash': str(x)} for x in xrange(10)]}))


@patch('wlffbd.blockchaininfo.urllib2.urlopen')
@patch('wlffbd.blockchaininfo.time.sleep')
def test_get_tx_from_online(mock_sleep, mock_urlopen):
    mock_urlopen.return_value = Mock()
    mock_urlopen.return_value.read.side_effect = ['{"n_tx": 9, "txs": [{"hash": "0"}, {"hash": "1"}, {"hash": "2"}]}'] * 3
    def _callback(txlist, n_tx):
        assert len(txlist) < n_tx
    blockchaininfo.get_tx_from_online('1234567890abcdef', limit=3, sleep=1, callback=_callback)
