#
#  target register data
#
REGISTER=data/registration-district/registration-district.tsv

#
#  source is primarily the gro-derived list
#
SOURCE=lists/gro-derived/list.tsv
HISTORICAL=lists/gro-district-book/list.tsv

MAPS=\
	maps/local-authority.tsv

FIXUPS=

# report of lists, maps and the register (TBD)
REPORT=report/index.html

# book of transfer of historical records
BOOK=book/index.html


all: $(REGISTER) $(MAPS) #$(BOOK)


#
#  currently made by hand ..
#
$(REGISTER):	bin/registration-district.py $(FIXUPS) $(SOURCE) $(HISTORICAL)
	@mkdir -p data/registration-district
	python3 bin/registration-district.py $(SOURCE) $(HISTORICAL) > $@


#
# maps
#
maps/local-authority.tsv: ../local-authority-data/maps/registration-district.tsv
	csvcut -tc local-authority,registration-district ../local-authority-data/maps/registration-district.tsv \
	| csvformat -T \
	> $@

#
# book
#
$(BOOK):	$(REGISTER) bin/book.py
	@mkdir -p book
	python3 bin/book.py > $@


# remove targets
clobber::
	rm -f $(REGISTER) $(DATA) $(MAPS)

#
#  python ..
#
init:
	[ -e $$(which csvcut) ] || pip install -r requirements.txt

flake8:
	flake8 bin

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
