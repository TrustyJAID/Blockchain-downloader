import sys
import json
import glob

for file in glob.glob("all*.txt"):
    with open(file, "rb") as infile:
        rows = (line.rstrip("\n").split("  ") for line in infile)
        xdict = {row[0]: row[1:] for row in rows}
        print(xdict)

    with open(file+".json", "wb") as outfile:
        json.dump(xdict, outfile)

