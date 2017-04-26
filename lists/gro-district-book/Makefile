URL='https://www.gro.gov.uk/gro/content/certificates/images/GRO%20Registration%20District%20Book.pdf'

# uses https://en.wikipedia.org/wiki/Pdftotext which is bundled with poppler https://en.wikipedia.org/wiki/Poppler_(software)

list.tsv:	data.tsv map.py
	./map.py < list.txt > $@

data.tsv:	data.txt squash.sh
	./squash.sh < data.txt > $@

data.txt:	data.pdf
	pdftotext -layout data.pdf $@

data.pdf:
	curl -s $(URL) > $@

clean:
	rm -f data.pdf data.txt list.tsv
