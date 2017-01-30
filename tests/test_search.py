# -*- coding: utf-8 -*-
'''search test functions'''

from wlffbd import search

import pytest


def test_check_magic():
    assert 'Julian Assange Found' == search.check_magic("01234567894a756c69616e20417373616e67650123456789")
    assert ' '.join('{} Found'.format(k) for k in list(search.DEFAULT_MAGIC.keys())) == search.check_magic(''.join(''.join(v) for v in list(search.DEFAULT_MAGIC.values())))


def test_check_hashes():
    assert 'pre-commitment 1: John Kerry' == search.check_hash("4bb96075acadc3d80b5ac872874c3037a386f4f595fe99e687439aabd0219809", "sha256")
    # assert ' '.join('{}'.format(k) for k in search.hashes['sha256'].keys()) == search.check_hash(''.join(''.join(v) for v in search.hashes['sha256'].values()), 'sha256')


def test_search_hashes():
    '''
    This method is obsolete with new hash dictionary
    assert 'pre-commitment 1: John Kerry sha256' == search.search_hashes("4bb96075acadc3d80b5ac872874c3037a386f4f595fe99e687439aabd0219809")
    assert 'robert-clayton-daniel-deposition.pdf.torrent md5' == search.search_hashes("d51c1b19202e62929adc999ba4585436")
    assert 'abschlussbericht-agnes.pdf sha1' == search.search_hashes("ed789b4e661f720bdcd467cf3ae2dd702c3304fe")
    assert '' == search.search_hashes("deadbeef")
    '''


def test_check_magic():
    assert 'Assange Found Julian Found Input' == search.search_hex("01234567894a756c69616e20417373616e67650123456789", "Input")
    assert 'Assange Found Julian Found Input reverse' == search.search_hex("896745230165676e61737341206e61696c754a8967452301", "Input")
    assert '' == search.search_hex("deadbeef", "Input")


def test_search_word():
    assert True == search.search_words(b"This is a test\n and some other words \x00 123456789")
    assert False == search.search_words(b"\xff\xff\xff\xff")
