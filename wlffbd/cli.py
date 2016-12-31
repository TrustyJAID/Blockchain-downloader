# -*- coding: utf-8 -*-
'''cli functions and package entry point'''


from . import blockchaininfo
from . import satoshi

import click

import argparse
import sys


@click.group()
def wlffbd():
    pass


@wlffbd.group('satoshi')
def cli_satoshi():
    '''Satoshi downloader and uploader functionality'''
    pass


@cli_satoshi.command('download-tx')
@click.argument('txid')
def satoshi_download_tx(txid):
    '''Download data from a single txid using satoshi method'''
    _, checksum, data = satoshi.length_checksum_data_from_rawdata(blockchain.rawdata_from_txid(txid))
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
