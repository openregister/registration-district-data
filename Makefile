
target: data/registration-district/registration-district.tsv

data/registration-district/registration-district.tsv: lists/gro-derived/list.tsv
	@mkdir -p data/registration-district
	cat lists/gro-derived/list.tsv > $@

clean:
	rm -f data/registration-district/registration-district.tsv
