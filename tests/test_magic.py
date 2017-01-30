# -*- coding: utf-8 -*-
'''magic test functions'''

from wlffbd import magic

import pytest

def test_check_magic():
    assert 'Julian Assange Found' == magic.check_magic("01234567894a756c69616e20417373616e67650123456789")
    assert ' '.join('{} Found'.format(k) for k in magic.DEFAULT_MAGIC.keys()) == magic.check_magic(''.join(''.join(v) for v in magic.DEFAULT_MAGIC.values()))
