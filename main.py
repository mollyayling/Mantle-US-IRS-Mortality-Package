from IRS_Mortality.IRS_Mortality import IRS_Mortality

# Set the required calc year
calc_year = 2030

# Instantiate IRS Table.
IRS_Mortality_O = IRS_Mortality(calc_year)
# Get full table as dict.
full_table = IRS_Mortality_O.full_table
print("Full table is", full_table)
# Get 430 Table as dict.
IRS_430_table = IRS_Mortality_O.IRS_430_table
print("430 Table is", IRS_430_table)
# Get 430 Static Table as dict.
IRS_430_static_table = IRS_Mortality_O.IRS_430_static_table
print("430 Static Table is", IRS_430_static_table)
# Get 417e Table as dict.
IRS_417e_table = IRS_Mortality_O.IRS_417e_table
print("417e Table is", IRS_417e_table)

