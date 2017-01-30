# -*- coding: utf-8 -*-
'''dlfn test functions'''

from wlffbd import dlfn

import pytest

import platform

def test_dlfn_init():
    d = dlfn.dlfn(None)
    assert 'file' == d.FILENAME


