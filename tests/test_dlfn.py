# -*- coding: utf-8 -*-
'''dlfn test functions'''

from wlffbd import dlfn

import pytest

import platform

def test_newline():
    assert platform.system() == 'Windows' and '\r\n' or '\n' == dlfn.newline()
