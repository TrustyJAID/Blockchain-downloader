
test:
	python blockchain_downloader.py `head -1 data/cablegate-addresses.txt`

clean:
	rm -f file fileo headerfiles.txt
