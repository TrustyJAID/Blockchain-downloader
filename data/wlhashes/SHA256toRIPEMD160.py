from binascii import unhexlify
import hashlib as h
import json
import glob


for file in glob.glob("*256sums.txt"):
    with open(file, "r") as infile:
        rows = (line.rstrip("\r\n").split("  ") for line in infile)
        xdict = {row[1]: h.new('ripemd160', unhexlify(row[0])).hexdigest() for row in rows}
        # print(xdict)

    with open(file.rsplit('.')[0]+".json", "wb") as outfile:
        json.dump(xdict, outfile)
