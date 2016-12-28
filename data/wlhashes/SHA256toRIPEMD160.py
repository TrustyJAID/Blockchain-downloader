from binascii import unhexlify
import hashlib as h
import sys
import json
import glob


for file in glob.glob("*256.txt"):
    with open(file, "rb") as infile:
        try:
            rows = (line.rstrip("\r\n").split("  ") for line in infile)
            xdict = {row[1]: h.new('ripemd160', unhexlify(row[0])).hexdigest() for row in rows}
            # print(rows)
        except TypeError:
            print(" One of the hashes is an odd-length in hex.")
            pass

    with open(file.rsplit('.')[0]+".json", "wb") as outfile:
        json.dump(xdict, outfile)
