
target: data/registration-district/registration-district.tsv maps/local-authority.tsv

data/registration-district/registration-district.tsv: lists/gro-derived/list.tsv
	@mkdir -p data/registration-district
	cat lists/gro-derived/list.tsv > $@

maps/local-authority.tsv: ../local-authority-data/maps/registration-district.tsv
	csvcut -tc local-authority,registration-district ../local-authority-data/maps/registration-district.tsv \
	| csvformat -T \
	> $@

clean:
	rm -f data/registration-district/registration-district.tsv
