URL='https://www.gro.gov.uk/gro/content/certificates/images/GRO%20Registration%20District%20Book.pdf'

# uses https://en.wikipedia.org/wiki/Pdftotext which is bundled with poppler https://en.wikipedia.org/wiki/Poppler_(software)

all: list.tsv abolished.tsv district.tsv

list.tsv:	data.tsv map.py
	python3 ./map.py < data.tsv > $@

data.tsv:	data.txt squash.sh
	./squash.sh < data.txt > $@

data.txt:	data.pdf
	pdftotext -layout data.pdf $@

data.pdf:
	curl -s $(URL) > $@

clean:
	rm -f data.pdf data.txt list.tsv
