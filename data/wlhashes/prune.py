import glob
import sys

with open(sys.argv[1], 'rb') as infile:
    rows = (line.rstrip("\r\n").split("  ") for line in infile)
    seen = set()
    dups = set()
    for row in rows:
        if row[0] in seen:
            if row[0] not in dups:
                dups.add(row[0])
        else:
            seen.add(row[0])
    print(dups)
    