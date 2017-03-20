
target: init data/registration-district/registration-district.tsv

data/registration-district/registration-district.tsv: ../local-authority-data/maps/registration-district.tsv
	@mkdir -p data/registration-district
	csvcut -tc registration-district,name,name-cy ../local-authority-data/maps/registration-district.tsv \
	| sed -E 's/$$/,,/g' \
	| sed 's/name-cy,,/name-cy,start-date,end-date/' \
	| csvsort \
	| csvformat -T \
	> $@

clean:
	rm -f data/registration-district/registration-district.tsv

init:
	[ -e $$(which csvcut) ] || pip install -r requirements.txt