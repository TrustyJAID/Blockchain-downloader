#
# File downloader
# Requires git://github.com/jgarzik/python-bitcoinrpc.git
#
# (c) 2013 Satoshi Nakamoto All Rights Reserved
#
# UNAUTHORIZED DUPLICATION AND/OR USAGE OF THIS PROGRAM IS PROHIBITED BY US AND INTERNATIONAL COPYRIGHT LAW

import sys
import os
import jsonrpc
import struct
from binascii import crc32, hexlify, unhexlify


if len(sys.argv) != 2:
    #print("""Usage: %s <txhash> """ % sys.argv[0], file=sys.stderr)
    #Set BTCRPCURL="http://User:Pass@localhost:8332"
    sys.exit()

proxy = jsonrpc.ServiceProxy(os.environ['BTCRPCURL'])

txid = sys.argv[1]

tx = proxy.getrawtransaction(txid,1)

data = b''
for txout in tx['vout'][0:-2]:
    for op in txout['scriptPubKey']['asm'].split(' '):
        if not op.startswith('OP_') and len(op) >= 40:
            data += unhexlify(op.encode('utf8'))

length = struct.unpack('<L', data[0:4])[0]
checksum = struct.unpack('<L', data[4:8])[0]
data = data[8:8+length]

if checksum != crc32(data):
    print('Checksum mismatch; expected %d but calculated %d' % (checksum, crc32(data)), file=sys.stderr)
    sys.exit()

sys.stdout.buffer.write(data)
