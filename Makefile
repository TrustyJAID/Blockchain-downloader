
test:
	python blockchain_downloader.py `head -1 data/cablegate-addresses.txt`
	python blockchain_downloader.py `head -1 data/wikileaks-addresses.txt`

clean:
	rm -f file fileo headerfiles.txt
	find . -type f -name '*~' -delete
