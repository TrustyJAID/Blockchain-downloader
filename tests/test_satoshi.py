# -*- coding: utf-8 -*-
'''satoshi test functions'''

from wlffbd import satoshi

import pytest


def test_unhexutf8():
    assert '\xab\xcd\xef' == satoshi.unhexutf8('abcdef')


def test_rawdata_from_jsonrpc_rawtx():
    message = 'Merry Christmas 2016 from Wiki Leaks Freedom Force'
    rawdata = b'2\x00\x00\x00\xd7E\x9a\xabMerry Christmas 2016 from Wiki Leaks Freedom Force'
    tx = {'vout': [{'scriptPubKey': {'asm': 'OP_' * 40}},
                   {'scriptPubKey': {'asm': 'OP_ ON_ POP_'}},
                   {'scriptPubKey': {'asm': satoshi.hexlify(satoshi.make_rawdata(message))}},
                   {},
                   {}]}
    assert rawdata == satoshi.rawdata_from_jsonrpc_rawtx(tx)


def test_length_checksum_data_from_rawdata_verify_checksum_data():
    rawdata = b'2\x00\x00\x00\xd7E\x9a\xabMerry Christmas 2016 from Wiki Leaks Freedom Force'
    message = 'Merry Christmas 2016 from Wiki Leaks Freedom Force'
    length, checksum, data = satoshi.length_checksum_data_from_rawdata(rawdata)
    assert 50 == length
    assert 2879014359 == checksum
    assert message == data
    assert satoshi.verify_checksum_data(checksum, data)
    assert satoshi.verify_rawdata(rawdata)
    assert (None, None, '00000') == satoshi.length_checksum_data_from_rawdata('00000')