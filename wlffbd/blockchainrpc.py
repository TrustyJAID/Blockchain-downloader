# -*- coding: utf-8 -*-
'''blockchain rpc related functions'''

import jsonrpclib

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 8332
DEFAULT_SCHEMA = 'http'


def make_server_from_url(url):
    '''Return a `jsonrpclib.Server` instance initialized with the given url'''
    return jsonrpclib.Server(url)


def make_server_url(username, password, hostname=DEFAULT_PORT, port=DEFAULT_PORT, schema=DEFAULT_SCHEMA):
    return '{schema}://{username}:{password}@{hostname}:{port}'.format(schema=schema,
                                                                       username=username,
                                                                       password=password,
                                                                       hostname=hostname,
                                                                       port=port)


def make_server(username, password, hostname=DEFAULT_HOSTNAME, port=DEFAULT_PORT, schema=DEFAULT_SCHEMA):
    return make_server_from_url(make_server_url(username=username,
                                                password=password,
                                                hostname=hostname,
                                                port=port,
                                                schema=schema))


                                                
