target: list.tsv \
	../../maps/gss.tsv

clean:
	rm -f list.tsv
	rm -f ../../maps/gss.tsv

GSS_LOCAL_AUTHORITY_MAP=../../../local-authority-data/maps/gss.tsv
REGISTRATION_DISTRICT_LOCAL_AUTHORITY_MAP=../../../local-authority-data/maps/registration-district.tsv

# Downloads "Registration Districts (December 2016) Names and Codes in England
# and Wales" (http://geoportal.statistics.gov.uk/datasets/ab365dcd27c64d04bcda8c5c019657a0_0)
# to list.tsv file.
list.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/ab365dcd27c64d04bcda8c5c019657a0_0.csv \
	| csvformat -T \
	| sed -e 's/REGD16NM/name/' -e 's/REGD16CD/gss/' \
	| tail --bytes=+4 \
	> $@

# Downloads "Ward to Registration District to Local Authority District
# (December 2016) Lookup in England and Wales" (https://geoportal.statistics.gov.uk/datasets/5a44fa3bc2894f968b711c194f74c2e7_0)
registration-district-map.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/5a44fa3bc2894f968b711c194f74c2e7_0.csv \
	| csvformat -T \
	> $@

# Downloads "Local Authority District to County (December 2016) Lookup in
# England" (https://geoportal.statistics.gov.uk/datasets/180a69233de94a8da3fb6a8a4959fcc7_0)
district-county-map.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/180a69233de94a8da3fb6a8a4959fcc7_0.csv \
	| csvformat -T \
	> $@

../../maps/gss.tsv: borough-and-unitary-map.tsv county-map.tsv
	csvstack borough-and-unitary-map.tsv county-map.tsv \
	| csvcut -tC registration-district-name \
	| csvformat -T \
	> $@

borough-and-unitary-map.tsv: registration-district-map.tsv $(GSS_LOCAL_AUTHORITY_MAP) \
	$(REGISTRATION_DISTRICT_LOCAL_AUTHORITY_MAP)

	./bin/add-local-authority-borough-code.sh > map-with-borough-local-authority.tsv
	./bin/add-registration-district-via-local-authority-borough-code.sh > $@
	rm -f map-with-borough-local-authority.tsv

county-map.tsv: registration-district-map.tsv district-county-map.tsv $(GSS_LOCAL_AUTHORITY_MAP) \
	$(REGISTRATION_DISTRICT_LOCAL_AUTHORITY_MAP)

	./bin/add-gss-county-code.sh > map-with-county-gss.tsv
	./bin/add-local-authority-county-code.sh > map-with-county-local-authority.tsv
	./bin/add-registration-district-via-local-authority-county-code.sh > $@
	rm -f map-with-county-gss.tsv
	rm -f map-with-county-local-authority.tsv
