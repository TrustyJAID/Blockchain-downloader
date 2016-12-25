# -*- coding: utf-8 -*-
'''dlfn test functions'''

from wlffbd import dlfn

import pytest

import platform

def test_newline():
    assert platform.system() == 'Windows' and '\r\n' or '\n' == dlfn.newline()


def test_dlfn_init():
    d = dlfn.dlfn(None)
    assert 'file' == d.FILENAME


def test_get_block_data():
    d = dlfn.dlfn(None)
    #assert d.SERVER.getblockhash(230010) == "000000000000015c28163515610010a24f6469e7741f83a9186393ff25bb8637"
    #assert d.SERVER.getblock("000000000000015c28163515610010a24f6469e7741f83a9186393ff25bb8637")['tx'][1] == "7f5d10bfdd7fff31eacdbc06ad4c6ec4005a6c6e3c73f205757941da81c88572"
    

def test_get_data_local():
    d = dlfn.dlfn(None)
    # assert d.INDIVIDUALFILE == False
