# -*- coding: utf-8 -*-
'''search test functions'''

from wlffbd import search

import pytest

def test_check_magic():
    assert 'Julian Assange Found' == search.check_magic("01234567894a756c69616e20417373616e67650123456789")
    assert ' '.join('{} Found'.format(k) for k in search.DEFAULT_MAGIC.keys()) == search.check_magic(''.join(''.join(v) for v in search.DEFAULT_MAGIC.values()))


# 34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039
# 4bb96075acadc3d80b5ac872874c3037a386f4f595fe99e687439aabd0219809
def test_check_hashes():
    assert 'pre-commitment 1: John Kerry' == search.check_hash("34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039", "sha256")
    # assert ' '.join('{}'.format(k) for k in search.hashes['sha256'].keys()) == search.check_hash(''.join(''.join(v) for v in search.hashes['sha256'].values()), 'sha256')
