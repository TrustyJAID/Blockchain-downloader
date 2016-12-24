# -*- coding: utf-8 -*-
'''cli functions and package entry point'''
from __future__ import print_function

from . import satoshi

import click

import argparse
import sys


@click.group()
def wlffbd():
    pass


@wlffbd.group('satoshi')
def cli_satoshi():
    pass


@cli_satoshi.command('download')
@click.argument('txid')
def satoshi_download(txid):
    '''Reimplementation of Satoshi-Downloader.py as subcommand of `wlffbd satoshi`'''
    # TODO: Implement local / remote blockchain data retrieval
    tx = {'vout': [{'scriptPubKey': {'asm': satoshi.hexlify(satoshi.make_rawdata('This is just a test! TODO: Make this real!'))}},
                   {},
                   {}]}
    rawdata = satoshi.rawdata_from_jsonrpc_rawtx(tx)
    length, checksum, data = satoshi.length_checksum_data_from_rawdata(rawdata)
    if satoshi.verify_checksum_data(checksum, data):
        sys.stdout.write(data)
    else:
        click.echo('{}: Checksum mismatch; expected {} but calculated {}'.format(click.style('Error', bold=True),
                                                                                 click.style(str(checksum), fg='red'),
                                                                                 click.style(str(satoshi.crc32(data) & 0xffffffff), fg='green')),
                   err=True)
        sys.exit(-1)
                   


@cli_satoshi.command('upload')
def satoshi_upload():
    click.echo('Uploading')
