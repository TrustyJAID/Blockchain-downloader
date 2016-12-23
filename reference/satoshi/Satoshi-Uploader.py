#
# File insertion tool for Bitcoin
# Requires git://github.com/jgarzik/python-bitcoinrpc.git
#
# (c) 2013 Satoshi Nakamoto All Rights Reserved
#
# UNAUTHORIZED DUPLICATION AND/OR USAGE OF THIS PROGRAM IS PROHIBITED BY US AND INTERNATIONAL COPYRIGHT LAW

import io
import jsonrpc
import os
import random
import struct
import sys
from binascii import crc32,hexlify,unhexlify
from decimal import Decimal

if len(sys.argv) < 5:
    print(\
"""\
Usage: %s <file> <dest addr> <dest amount> {<fee-per-kb>}
Set BTCRPCURL=http://user:pass@localhost:portnum""" % sys.argv[0], file=sys.stderr)
    sys.exit()

COIN = 100000000

def unhexstr(str):
    return unhexlify(str.encode('utf8'))

proxy = jsonrpc.ServiceProxy(os.environ['BTCRPCURL'])

def select_txins(value):
    unspent = list(proxy.listunspent())
    random.shuffle(unspent)

    r = []
    total = 0
    for tx in unspent:
        total += tx['amount']
        r.append(tx)

        if total >= value:
            break

    if total < value:
        return None
    else:
        return (r, total)

def varint(n):
    if n < 0xfd:
        return bytes([n])
    elif n < 0xffff:
        return b'\xfd' + struct.pack('<H',n)
    else:
        assert False

def packtxin(prevout, scriptSig, seq=0xffffffff):
    return prevout[0][::-1] + struct.pack('<L',prevout[1]) + varint(len(scriptSig)) + scriptSig + struct.pack('<L', seq)

def packtxout(value, scriptPubKey):
    return struct.pack('<Q',int(value*COIN)) + varint(len(scriptPubKey)) + scriptPubKey

def packtx(txins, txouts, locktime=0):
    r = b'\x01\x00\x00\x00' # version
    r += varint(len(txins))

    for txin in txins:
        r += packtxin((unhexstr(txin['txid']),txin['vout']), b'')

    r += varint(len(txouts))

    for (value, scriptPubKey) in txouts:
        r += packtxout(value, scriptPubKey)

    r += struct.pack('<L', locktime)
    return r

OP_CHECKSIG = b'\xac'
OP_CHECKMULTISIG = b'\xae'
OP_PUSHDATA1 = b'\x4c'
OP_DUP = b'\x76'
OP_HASH160 = b'\xa9'
OP_EQUALVERIFY = b'\x88'
def pushdata(data):
    assert len(data) < OP_PUSHDATA1[0]
    return bytes([len(data)]) + data

def pushint(n):
    assert 0 < n <= 16
    return bytes([0x51 + n-1])


def addr2bytes(s):
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = 0
    for c in s:
        n *= 58
        if c not in digits58:
            raise ValueError
        n += digits58.index(c)

    h = '%x' % n
    if len(h) % 2:
        h = '0' + h

    for c in s:
        if c == digits58[0]:
            h = '00' + h
        else:
            break
    return unhexstr(h)[1:-4] # skip version and checksum

def checkmultisig_scriptPubKey_dump(fd):
    data = fd.read(65*3)
    if not data:
        return None

    r = pushint(1)

    n = 0
    while data:
        chunk = data[0:65]
        data = data[65:]

        if len(chunk) < 33:
            chunk += b'\x00'*(33-len(chunk))
        elif len(chunk) < 65:
            chunk += b'\x00'*(65-len(chunk))

        r += pushdata(chunk)
        n += 1

    r += pushint(n) + OP_CHECKMULTISIG
    return r


(txins, change) = select_txins(0)

txouts = []

data = open(sys.argv[1],'rb').read()
data = struct.pack('<L', len(data)) + struct.pack('<L', crc32(data)) + data
fd = io.BytesIO(data)

while True:
    scriptPubKey = checkmultisig_scriptPubKey_dump(fd)

    if scriptPubKey is None:
        break

    value = Decimal(1/COIN)
    txouts.append((value, scriptPubKey))

    change -= value

# dest output
out_value = Decimal(sys.argv[3])
change -= out_value
txouts.append((out_value, OP_DUP + OP_HASH160 + pushdata(addr2bytes(sys.argv[2])) + OP_EQUALVERIFY + OP_CHECKSIG))

# change output
change_addr = proxy.getnewaddress()
txouts.append([change, OP_DUP + OP_HASH160 + pushdata(addr2bytes(change_addr)) + OP_EQUALVERIFY + OP_CHECKSIG])

tx = packtx(txins, txouts)
signed_tx = proxy.signrawtransaction(hexlify(tx).decode('utf8'))

FEEPERKB = Decimal(0.001)
try:
    FEEPERKB = Decimal(sys.argv[4])
except IndexError:
    pass
fee = Decimal(len(signed_tx['hex'])/1000) * FEEPERKB
change -= fee
txouts[-1][0] = change

tx = packtx(txins, txouts)
signed_tx = proxy.signrawtransaction(hexlify(tx).decode('utf8'))
assert signed_tx['complete']

print('Size: %d  Fee: %2.8f' % (len(signed_tx['hex'])/2,fee),file=sys.stderr)

if False:
    print(proxy.sendrawtransaction(signed_tx['hex']))
else:
    print(signed_tx)