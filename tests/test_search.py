# -*- coding: utf-8 -*-
'''search test functions'''

from wlffbd import search

import pytest

def test_check_magic():
    assert 'Julian Assange Found' == search.check_magic("01234567894a756c69616e20417373616e67650123456789")
    assert ' '.join('{} Found'.format(k) for k in search.DEFAULT_MAGIC.keys()) == search.check_magic(''.join(''.join(v) for v in search.DEFAULT_MAGIC.values()))


def test_check_hashes():
    assert 'pre-commitment 1: John Kerry' == search.check_hash("34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039", "sha256")
    # assert ' '.join('{}'.format(k) for k in search.hashes['sha256'].keys()) == search.check_hash(''.join(''.join(v) for v in search.hashes['sha256'].values()), 'sha256')

def test_search_hashes():
    assert 'pre-commitment 1: John Kerry sha256' == search.search_hashes("34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039")
    assert 'robert-clayton-daniel-deposition.pdf.torrent md5' == search.search_hashes("6435316331623139323032653632393239616463393939626134353835343336")
    assert 'abschlussbericht-agnes.pdf sha1' == search.search_hashes("65643738396234653636316637323062646364343637636633616532646437303263333330346665")
    assert '' == search.search_hashes("deadbeef")

def test_check_magic():
    assert 'Julian Assange Found Input' == search.search_hex("01234567894a756c69616e20417373616e67650123456789", "Input")
    assert 'Julian Assange Found Input reverse' == search.search_hex("896745230165676e61737341206e61696c754a8967452301", "Input")
    assert '' == search.search_hex("deadbeef", "Input")
