target: list.tsv

GRO_OFFICE_LIST=../../../register-office-data/lists/gro-list/list.tsv

list.tsv: $(GRO_OFFICE_LIST)
	csvcut -tc registration-district,registration-district-name $(GRO_OFFICE_LIST) \
	| sed 's/registration-district,registration-district-name/registration-district,name/' \
	| uniq \
	| csvformat -T \
	> $@

clean:
	rm -f list.tsv
