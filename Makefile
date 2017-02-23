
target: data/registration-district/registration-district.tsv

data/registration-district/registration-district.tsv: ../local-authority-data/maps/registration-district.tsv
	@mkdir -p data/registration-district
	csvcut -tc registration-district,name,local-authority ../local-authority-data/maps/registration-district.tsv \
	| sed 's/name,local-authority/name,local-authority,start-date,end-date/' \
	| sed -E 's/([A-Z][A-Z][A-Z])$$/\1,,/g' \
	| csvformat -T \
	> $@

clean:
	rm -f data/registration-district/registration-district.tsv
