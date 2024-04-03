"""This module contains the IRS_Mortality class which represents the IRS mortality rate table for a given calculation year."""

from . import pri_2012, MP_2021_Adj_Females, MP_2021_Adj_Males, projection_years, published_430, blending_table, published_417e
from math import prod, ceil, floor
import decimal
from typing import Dict


class IRS_Mortality:
    """This class represents an IRS Mortality table for a given calculation year.
    
    If the IRS have published their rates for the given calculation year, the 
    published rates are returned, otherwise they are calculated. 

    The IRS have published their rates up to 2024. There are three types of rate:

    1. IRS 430 rates (Male EE, Male HA, Female EE, Female HA)
    2. IRS 430 static rates (Male, Female)
    3. IRS 417e rates
    
    attributes:
    -----------
    calc_year : int
        The calculation year for the IRS mortality rates.
    published : bool
        A boolean indicating whether the IRS rates are published for the given calculation year.
        
    methods:
    --------
    full_table() 
        Get the full IRS Mortality table (430, 430 static & 417e) for the calculation year.
    IRS_430_table() 
        Get the full IRS 430 table for the calculation year.
    IRS_430_static_table() 
        Get the full IRS 430 static table for the calculation year.
    IRS_417e_table()
        Get the full IRS 417e table for the calculation year.
    """
    # Minimum and maximum years for which IRS Mortality rates are defined.
    max_year = 2099
    min_year = 2009

    # The base table used for IRS mortality calculations (from 2024) is the Pri-2012.
    base_table = pri_2012
    base_table, base_year = base_table.load()

    # The improvement tables used for IRS mortality calculations (from 2024) are the MP2021 Adjusted Tables.
    improvement_table = {"Male": MP_2021_Adj_Males.load(), "Female": MP_2021_Adj_Females.load()}
    end_improvement_year = list(improvement_table["Male"].keys())[-1]
    start_improvement_age = list(improvement_table["Male"][end_improvement_year].keys())[0]

    projection_years = projection_years.load()

    # IRS have been published tables up to 2024. 
    published_years = list(range(2009, 2025))
    published_430_table, published_static_table = published_430.load()
    published_417e_table = published_417e.load()

    # Blending table used for IRS static rates.
    blending_table = blending_table.load()

    # Number of decimal places to round to.
    rounding = 5

    # Types of IRS 430 Rates.
    types_430 = ["Male EE", "Male HA", "Female EE", "Female HA"]

    # Ages for which IRS rates are defined.
    ages = list(range(15, 121))

    def __init__(self, calc_year : int):
        """Initialise IRS_Mortality table with calculation year and published status."""
        if calc_year > IRS_Mortality.max_year or calc_year < IRS_Mortality.min_year:
            raise ValueError((f"IRS Mortality rates are not defined for {calc_year}. "
                              "Calc year must be between 2009 and 2099."))
        self.calc_year = calc_year
        self.published = True if self.calc_year in IRS_Mortality.published_years else False
    
    @property
    def full_table(self):
        """Get full IRS Mortality Table for the calculation year."""
        return {"430 Table": self.IRS_430_table, "430 Static Table": self.IRS_430_static_table, "417e Table": self.IRS_417e_table}
        
    @property
    def IRS_430_table(self) -> Dict[str, Dict[int, float]]:
        """Get full IRS 430 table for the calculation year.
        
        Calculate and return tables if tables have not been published,
        otherwise return published tables.
        """
        if self.published:
            return IRS_Mortality.published_430_table[self.calc_year]
        else:
            return self._calculate_430_table()
    
    @property
    def IRS_430_static_table(self) -> Dict[str, Dict[int, float]]:
        """Get full IRS 430 static table for the calculation year.
        
        Calculate and return tables if tables have not been published,
        otherwise return published tables.
        """
        if self.published:
            return IRS_Mortality.published_static_table[self.calc_year]
        else:
            return self._calculate_430_static_table()
        
    @property
    def IRS_417e_table(self) -> Dict[int, float]:
        """Get full IRS 417e table for the calculation year.
        
        Calculate and return tables if tables have not been published,
        otherwise return published tables.
        """
        if self.published:
            return IRS_Mortality.published_417e_table[self.calc_year]
        else:
            return self._calculate_417e_table()
    
    @staticmethod
    def _excel_round(number : float, digits: int):
        """Round a number to a given number of digits using Excel (standard)
        rounding (private method).
        
        This method uses the ROUND_HALF_UP rounding method from the decimal 
        module to round a number to a given number of digits. This is in 
        contrast to the Python round() method that implements bankers rounding.
        """
        context = decimal.getcontext()
        context.rounding = decimal.ROUND_HALF_UP
        d = decimal.Decimal(str(number))
        return float(d.quantize(decimal.Decimal('1.' + '0' * digits)))    

    def _calculate_430_table(self):
        """Calculate IRS 430 table (private method)."""
        table = {}
        for type in IRS_Mortality.types_430:
            table[type] = {}
            for age in IRS_Mortality.ages:
                # Get calc parameters
                base_rate = IRS_Mortality.base_table[type][age]
                sex = type.split(" ")[0]
                improvement_table = IRS_Mortality.improvement_table[sex]
                projection_years = IRS_Mortality.projection_years[type][age]
                projection_years_trunc = int(projection_years)
                
                # Calculate lower rate
                improvements_lower = prod([(1-improvement_table[IRS_Mortality.base_year + 1 + i][age]) for i in range(self.calc_year - IRS_Mortality.base_year + projection_years_trunc)])
                lower_rate = IRS_Mortality._excel_round(base_rate * improvements_lower, 6)
                
                # Calculate higher rate
                improvements_higher = prod([(1-improvement_table[IRS_Mortality.base_year + 1 + i][age]) for i in range(self.calc_year - IRS_Mortality.base_year + projection_years_trunc + 1)])
                higher_rate = IRS_Mortality._excel_round(base_rate * improvements_higher, 6)

                # Interpolate between higehr and lower rates
                remainder = projection_years % 1
                rate = (1 - remainder) * lower_rate + remainder * higher_rate
                table[type][age] = IRS_Mortality._excel_round(rate, 6)
        return table
        
    def _calculate_430_static_table(self):
        """Calculate IRS 430 static table (private method)."""
        table_430 = self._calculate_430_table()
        table = {}
        for sex in ["Male", "Female"]:
            table[sex] = {}
            for age in IRS_Mortality.ages:
                blending = IRS_Mortality.blending_table[sex][age]
                EE_type = sex + " EE"
                HA_type = sex + " HA"
                static_rate = table_430[HA_type][age] * blending + table_430[EE_type][age] * (1 - blending)
                table[sex][age] = IRS_Mortality._excel_round(IRS_Mortality._excel_round(static_rate, 6), IRS_Mortality.rounding)
        return table
    
    def _calculate_417e_table(self):
        """Calculate IRS 417e table (private method)."""
        table_static_430 = self._calculate_430_static_table()
        table = {}
        for age in IRS_Mortality.ages:
            table[age] = IRS_Mortality._excel_round((table_static_430["Male"][age] + table_static_430["Female"][age])/2, IRS_Mortality.rounding)
        return table
    