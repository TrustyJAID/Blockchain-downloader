# https://gist.github.com/anonymous/063ad09f3be66ca53f69b1e44304e4b3
#  jean.py Python3 compatible   --     https://gist.github.com/anonymous/063ad09f3be66ca53f69b1e44304e4b3
#  like http://pastebin.com/raw/mCqDxt6e  but no fucking captchas

import sys
import pycurl
import struct
from binascii import unhexlify, crc32
from urllib.request import urlopen

transaction = str(sys.argv[1])
data = urlopen("https://blockchain.info/tx/"+transaction+"?show_adv=true")
dataout = b''
atoutput = False

for line in data:

if b'Output Scripts' in line:
atoutput = True

if b'</table>' in line:
atoutput = False

if atoutput:
if len(line) > 100:
chunks = line.split(b' ')
for c in chunks:
if b'O' not in c and b'\n' not in c and b'>' not in c and b'<' not in c:
dataout += unhexlify(c)

length = struct.unpack('<L', dataout[0:4])[0]
checksum = struct.unpack('<L', dataout[4:8])[0]
dataout = dataout[8:8+length]

sys.stdout.buffer.write(dataout)
