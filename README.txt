IRS Mortality Package
---------------------

This package is designed to produce IRS mortality rates for a given calculation year. This package replicates the "IRC 430-417e table development.xlsx" workbook. 
For info this workbook can be found at ./Data/Source Workbook/IRC 430-417e table development.xlsx although data is not directly pulled from it.

If the IRS have published their rates for the given calculation year, the published rates are returned, otherwise they are calculated. 

The IRS have published their rates up to 2024. There are three types of rate:

1. IRS 430 rates (Male EE, Male HA, Female EE, Female HA)
2. IRS 430 static rates (Male, Female)
3. IRS 417e rates

Rates are defined for ages 15 up to 120 and for calculation years from 2009 to 2099.

All tables in this package are read-in and returned as Python dictionaries.

Data
-----

From 2024, IRS Rates are calculated using the Pre-2012 base table, MP 2021 adjusted improvement tables and a specified Projection Years methodology.
The 430 static rates are calculated using a specified blending methodology. 
The published 430, 430 static and 417e rates are used for calculation years post 2024.

This data can all be found within the ./Data folder as csv files. The published 430 and 430 static rates are contained within the same files.

Tables Package
--------------------

Contains the classes for each type of data table used in the calculation. Each class is a sub-class of the table class.

The improvement table class extends the improvement rates to the required year and age by extrapolating using the nearest rates in the table (in line with the workbook's functionality). 

IRS Mortality Package
---------------------

The ./IRS_Mortality package contains the IRS_Mortality class, which is instantiated to represent a table of IRS Mortality rates at a given calculation date.

The table represents published rates if the calculation year is a published year, otherwise it calculates them.

This class implements excel rounding (rounding half up) in order to achieve the same post-rounding rates as the workbook.
 
The IRS mortality object holds the 430, 430 static and 417e tables as properties, as well as the full table of all these rates. 

Please see the main.py file for an example of how to use this package.

