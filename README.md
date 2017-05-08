# Registration district data

Data for an alpha register of registration districts in England and Wales.

  * [data/registration-district/registration-district.tsv](data/registration-district/registration-district.tsv)

## Legislation

Legislation referencing registration districts includes:

  * [Registration Service Act 1953 (c. 37), Sch 5](http://www.legislation.gov.uk/ukpga/Eliz2/1-2/37/section/5?view=plain)

# Lists, fixes and maps

You can see a report generated from the lists, fixes and maps in this repository: https://openregister.github.io/registration-district-data/report/

Generating maps is somewhat complicated by the same code being used historically to indicate different registration districts and much of the data being maintained in PDF documents.

This list of lists is by no means comprehensive, and contributions of other lists are appreciated.

## Generating data

Use make to generate register shaped data and the reports:

```
make init
make
```
