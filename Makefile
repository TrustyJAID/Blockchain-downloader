
test:
	python blockchain_downloader.py data/cablegate-addresses.txt
	python blockchain_downloader.py `head -1 data/wikileaks-addresses.txt`

clean:
	rm -f file fileo headerfiles.txt
	rm -f file.txt filein.txt fileorig.txt
	find . -type f -name '*~' -delete
