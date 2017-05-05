# Registration district data

Data for an alpha register of registration districts in England and Wales.

  * [data/registration-district/registration-district.tsv](data/registration-district/registration-district.tsv)

## Legislation

Legislation referencing registration districts includes:

  * [Registration Service Act 1953 (c. 37), Sch 5](http://www.legislation.gov.uk/ukpga/Eliz2/1-2/37/section/5?view=plain)

## Maps

Maps assist in the translation of existing codes and names to register records:

| Map | Fields |
| :---         |    :--- |
| [gss](maps/gss.tsv) |GSS code and name for registration districts in England and Wales |

## Lists

The data has been compiled from existing lists of registration districts found
in a number of different government datasets:

| List | Source | Count |
| :---         |    :--- | ---: |
|[gro](lists/gro) |Registration districts from General Register Office internal list 2015, including 5 abolished districts.|[180](lists/gro/list.tsv)|
|[gro-derived](lists/gro-derived) |Registration districts from General Register Office internal list 2015, with names converted to mixed case, added Welsh name field, and end date on abolished districts.|[180](lists/gro-derived/list.tsv)|
|[gro-district-book](lists/gro-district-book) |Registration districts from General Register Office (historical book)[https://www.gro.gov.uk/gro/content/certificates/images/GRO%20Registration%20District%20Book.pdf]|[1057](lists/gro-district-book/list.tsv)|
|[gro-officers](lists/gro-officers) |Registration districts extracted from General Register Office internal officer office list.|[175](lists/gro-officers/list.tsv)|
|[ons](lists/ons) |[Registration Districts (December 2016) Names and Codes in England and Wales](http://geoportal.statistics.gov.uk/datasets/ab365dcd27c64d04bcda8c5c019657a0_0) from ONS Geography Open Data. Contains National Statistics data © Crown copyright and database right 2016.|[175](lists/ons/list.tsv)|

## Generating data

Use make to generate register shaped data:

```
make init
make
```
