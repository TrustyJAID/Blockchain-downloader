import sys
import json
import glob

for file in glob.glob("all*.txt"):
    with open(file, "rb") as infile:
        rows = (line.rstrip("\r\n").split("  ") for line in infile)
        xdict = {row[1]: row[0] for row in rows}
        print(xdict)

    with open(file.rsplit('.')[0]+".json", "wb") as outfile:
        json.dump(xdict, outfile)

