#
#  target register data
#
REGISTER=data/registration-district/registration-district.tsv

#
#  source is the gro-register list
#
SOURCE=lists/gro-register/list.tsv
HISTORICAL=lists/book-historical/list.tsv

MAPS=\
	maps/name.tsv\
	maps/local-authority.tsv

LISTS=\
	lists/book-abolished/list.tsv\
	lists/book-historical/list.tsv\
	lists/book-transfers/list.tsv\
	lists/gro-2015/list.tsv\
	lists/gro-register/list.tsv\
	lists/gro-officers/list.tsv\
	lists/ons/list.tsv

FIXUPS=\
	fixup/name.tsv


# report of lists, maps and the register (TBD)
REPORT=report/index.html

# recreation of the book of transfer of historical records
BOOK=book/index.html


all: $(REGISTER) $(MAPS) $(REPORT)


#
#  made by hand ..
#
$(REGISTER):	bin/registration-district.py $(FIXUPS) $(SOURCE)
	@mkdir -p data/registration-district
	python3 bin/registration-district.py $(SOURCE) > $@


#
#  maps
#
maps/name.tsv:	$(REGISTER) fixup/name.tsv $(LISTS) lists/index.yml bin/name.py
	@mkdir -p maps
	python3 bin/name.py fixup/name.tsv < $(REGISTER) > $@

maps/local-authority.tsv: ../local-authority-data/maps/registration-district.tsv
	csvcut -tc local-authority,registration-district ../local-authority-data/maps/registration-district.tsv \
	| csvformat -T \
	> $@

#
# report
#
$(REPORT):	$(REGISTER) $(LISTS) $(MAPS) maps/index.yml lists/index.yml bin/report.py
	@mkdir -p report
	python3 bin/report.py > $@

#
#  demonstration, recreate book
#
$(BOOK):	$(REGISTER) bin/book.py
	@mkdir -p book
	python3 bin/book.py > $@


#  remove targets
clobber::
	rm -f $(REGISTER) $(DATA) $(MAPS)

#
#  python ..
#
init:
	pip install -r requirements.txt

flake8:
	flake8 bin

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
