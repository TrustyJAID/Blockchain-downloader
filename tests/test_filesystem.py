# -*- coding: utf-8 -*-
'''dlfn test functions'''

from wlffbd import filesystem
from mock import patch, mock_open

from StringIO import StringIO

import pytest

# TODO: Figure out why decorator version doesn't work for this
def test_read():
    with patch('wlffbd.filesystem.open', mock_open(read_data='Test string')):
        assert 'Test string' == filesystem.read('<nofile>')


@patch('wlffbd.filesystem.sys.stderr', new_callable=StringIO)
def test_read_fail(mock_stderr):
    filesystem.read('NOFILE')
    assert len(mock_stderr.getvalue())


# TODO: Figure out why decorator version doesn't work for this
def test_readlines():
    with patch('wlffbd.filesystem.open', mock_open(read_data='Test string\n' * 10)):
        assert 10 == len(filesystem.readlines('<nofile>'))


@patch('wlffbd.filesystem.sys.stderr', new_callable=StringIO)
def test_readlines_fail(mock_stderr):
    filesystem.readlines('NOFILE')
    assert len(mock_stderr.getvalue())


@patch('wlffbd.filesystem.open')
def test_write(mock_file):
    mock_file = mock_open()
    assert 'Test string' == filesystem.write('<nofile>', 'Test string')


@patch('wlffbd.filesystem.sys.stderr', new_callable=StringIO)
def test_write_fail(mock_stderr):
    assert None == filesystem.write('', '')
    assert len(mock_stderr.getvalue())

def test_newline():
    assert platform.system() == 'Windows' and '\r\n' or '\n' == filesystem.newline()

