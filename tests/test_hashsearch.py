# -*- coding: utf-8 -*-
'''hashsearch test functions'''

from wlffbd import hashsearch

import pytest

# 34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039
# 4bb96075acadc3d80b5ac872874c3037a386f4f595fe99e687439aabd0219809
def test_check_hashes():
    assert 'pre-commitment 1: John Kerry' == hashsearch.check_hash("34626239363037356163616463336438306235616338373238373463333033376133383666346635393566653939653638373433396161626430323139383039", "sha256")
    # assert ' '.join('{}'.format(k) for k in hashsearch.hashes['sha256'].keys()) == hashsearch.check_hash(''.join(''.join(v) for v in hashsearch.hashes['sha256'].values()), 'sha256')
